import sys

import pandas as pd
import numpy as np
from scipy.stats import norm

from src.curves.curve import Curve, get_curve, copy_curve

from src.dates.date import Date, Days, Years

from src.assets.products import Portfolio
import src.assets.products as pricers

from src.liabilities.liabilities import Liabilities, LiabilitiesUK

from src.Plan.Plan import Plan

from src.simulation.sim_factor import randCor
from src.simulation.factor import Factor, copy_factor, get_factor
import src.simulation.models as models

if (len(sys.argv) == 1): sys.argv = sys.argv + ['Portugal/PT_config.xlsx']

# if (len(sys.argv) == 1): sys.argv = sys.argv + ['Germany/DE_config.xlsx']
# if (len(sys.argv) == 1): sys.argv = sys.argv + ['UK/UK_config.xlsx']
# if (len(sys.argv) == 1): sys.argv = sys.argv + ['Spain/ES_config.xlsx']
# if (len(sys.argv) == 1): sys.argv = sys.argv + ['Brazil/BR_config.xlsx']
# if (len(sys.argv) == 1): sys.argv = sys.argv + ['Portugal/PT_config.xlsx']

print("Reading file: '", sys.argv[1], "'",  sep="")

#### READING CONFIGURATION FILE ####

try:
    data = pd.read_excel(sys.argv[1], sheet_name='main')
except FileNotFoundError:
    print("Error when reading the file: '" + sys.argv[1] + "'")


#### SETTING CONFIGURATION VAR ####

data.valuation_date = data.valuation_date.apply(lambda x: Date(x.day, x.month, x.year))
data.t              = data.t.apply(lambda x: eval(x))

config = data.to_dict(orient='records')[0]


#### SETTING SIMULATION PARAMETERS ####

params = { }

params['sheets'] = pd.ExcelFile(sys.argv[1]).sheet_names

params['liabilities']    = True if 'liabilities'    in params['sheets']                         else False
params['mortality_risk'] = True if 'mortality_risk' in params['sheets']                         else False
params['factors']        = True if 'factors'        in params['sheets']                         else False
params['curves']         = True if 'curves'         in params['sheets']                         else False

params['assets']         = True if 'Assets'         in pd.ExcelFile(config['file']).sheet_names else False


## Reading Liabilities

if params['liabilities']:
    print("Reading liabilities configuration...", end="")
    config['liabilities'] = pd.read_excel(sys.argv[1], sheet_name='liabilities').to_dict(orient='records')[0]
    print("OK")

if params['mortality_risk']:
    print("Reading mortality risk configuration...", end="")
    config['mortality_risk'] = pd.read_excel(sys.argv[1], sheet_name='mortality_risk').to_dict(orient='records')[0]
    print("OK")

if params['factors']:
    print("Reading factors parameters...", end="")
    imp_factors = pd.read_excel(sys.argv[1], sheet_name='factors')
    imp_factors['params'] = imp_factors.drop('model', axis=1).apply(lambda x: x.to_dict(), axis=1)
    config['factors'] = imp_factors[['model', 'params']].to_dict(orient='index')
    print("OK")
    print("\tFactors:", [i for i in config['factors'].keys()])
    print("\tThe next factors will be simulated:", [i for i in imp_factors[imp_factors.flag].index])


if params['curves']:
    print("Reading curves configuration...", end="")
    imp_curves = pd.read_excel(sys.argv[1], sheet_name='curves')
    imp_curves['params'] = imp_curves.drop('model', axis=1).apply(lambda x: x.to_dict(), axis=1)
    config['curves'] = imp_curves[['model', 'params']].to_dict(orient='index')
    print("OK")
    print("\tCurves:", [i for i in config['curves'].keys()])
    print("\tThe next curves will be simulated:", [i for i in imp_curves[imp_curves.flag].index])


#### SET SEED ####

print("\tSet seed:", config['seed'])
np.random.seed(config['seed'])

##### LOAD CURVES ####

if params['curves']:
    print("Reading curves data...", end="")
    curves = pd.read_excel(config['file'], sheet_name="Curves")
    curves.Tenor = curves.Tenor.apply(lambda x: config['valuation_date'] + Days(x))
    curves = curves.groupby('Name').\
        apply(lambda x: Curve(name=str(x.Name.unique()[0]),
                              dates=x.Tenor.tolist(),
                              rates=x.Rate.tolist()))
    print("OK")


#### LOAD PORTFOLIO ####

if params['assets']:
    print("Reading assets data...", end="")
    a = pd.read_excel(config['file'], sheet_name="Assets")
    a[a.select_dtypes(include=['datetime']).columns] = \
        a[a.select_dtypes(include=['datetime']).columns].\
        applymap(lambda x: Date(x.day, x.month, x.year))
    print("OK")

if params['curves']:
    print("Extrapolating curves...", end="")
    for c in curves.index:
        pos = np.where((a.curve_irr == c) * [1] == 1)[0].tolist()
        if pos:
            zzz = int(max(a.matDate[pos]).year())
        else:
            zzz = int(config['valuation_date'].year())
        zzz = max(zzz, curves[c].dates[-1].year()+1)
        reqyears = int(max(zzz - config['valuation_date'].year(), int(config['liabilities']['duration'] / 365) + 1))
        curves[c].extrapolationCDS(rf=config['rf'], RR=config['RR'], reqyears=reqyears,
                                   val_date=config['valuation_date'])
    print("OK")


if params['curves']:
    sim_curves = [0] * len(curves)
    for i in range(0, len(curves)):
        sim_curves[i] = copy_curve(curves[i])
    sim_curves = pd.Series(sim_curves)
    sim_curves.index = curves.index
    simulator_curves = {k: getattr(models, v['model'])(curve=get_curve(k, curves),
                                                       val_date=config['valuation_date'],
                                                       t=config['t'],
                                                       **v['params']) for k, v in config['curves'].items()}
    simulator_curves = pd.Series(simulator_curves)


#### LOAD FACTORS ####

if params['factors']:
    factors = pd.Series(map(lambda x: Factor(name=x), list(config['factors'].keys())))
    factors.index = config['factors'].keys()
    sim_factor = [0] * len(factors)
    for i in range(0, len(factors)):
        sim_factor[i] = copy_factor(factors[i])
    sim_factor = pd.Series(sim_factor)
    sim_factor.index = factors.index
    for i in config['factors'].keys():
        config['factors'][i]['params']['curve'] = get_curve(config['factors'][i]['params']['curve'], curves)
    simulator_factors = {k: getattr(models, v['model'])(factor=factors[k],
                                                        val_date=config['valuation_date'],
                                                        t=config['t'],
                                                        **v['params']) for k, v in config['factors'].items()}
    simulator_factors = pd.Series(simulator_factors)


#### PORTFOLIO CONSTRUCTION ####

if params['assets']:
    print("Reading assets data...", end="")
    a['curve_irr'] = a['curve_irr'].apply(lambda x: get_curve(x, sim_curves))
    a['curve_spread'] = a['curve_spread'].apply(lambda x: get_curve(x, sim_curves))
    if params['factors']: a['factor'] = a['factor'].apply(lambda x: get_factor(x, sim_factor))
    a['args'] = a.drop(['Pais', 'Plan', 'pricer'], axis=1).\
        apply(lambda x: x.to_dict(), axis=1)
    a = a[['Pais', 'Plan', 'pricer', 'args']]
    a["Portfolio"] = a.apply(lambda x: getattr(pricers, x['pricer'])(val_date=config['valuation_date'],
                                                                     t=config['t'],
                                                                     **x['args']), axis=1)
    a = a[['Pais', 'Plan', 'Portfolio']].\
        groupby(['Pais', 'Plan']).\
        agg(Portfolio.create_portfolio).Portfolio
    print("OK")


#### LOAD LIABILITIES ####

if params['liabilities']:
    l = pd.read_excel(config['file'], sheet_name="Liabilities")
    l[l.select_dtypes(include=['datetime']).columns] = \
        l[l.select_dtypes(include=['datetime']).columns]. \
            applymap(lambda x: Date(x.day, x.month, x.year))
    if config['liabilities']['type'] == 'LiabilitiesUK':
        l = l.groupby(['Pais', 'Plan']). \
            apply(lambda x: LiabilitiesUK(val_date=config['valuation_date'],
                                          dates=x.FechaCF.tolist(),
                                          active=x.Active,
                                          deferred=x.Deferred,
                                          pensioner=x.Pensioner,
                                          RLPI=pd.read_excel(sys.argv[1], sheet_name=config['liabilities']['table_sheet']),
                                          curve_irr=get_curve(config['liabilities']['curve_irr'], sim_curves),
                                          curve_spread=get_curve(config['liabilities']['curve_spread'], sim_curves),
                                          curve_inf=get_curve(config['liabilities']['curve_inf'], sim_curves)))
    else:
        l = l.groupby(['Pais', 'Plan']). \
            apply(lambda x: Liabilities(val_date=config['valuation_date'],
                                        dates=x.FechaCF.tolist(),
                                        flows=x.CF.tolist(),
                                        curve_irr=get_curve(config['liabilities']['curve_irr'], sim_curves),
                                        curve_spread=get_curve(config['liabilities']['curve_spread'], sim_curves),
                                        curve_inf=get_curve(config['liabilities']['curve_inf'], sim_curves)))


#### CREATE PLANS ###

def nullPortfolios(list):
    x = [0] * len(list)
    for i in range(0, len(list)):
        if pd.isna(list[i]):
            x[i] = Portfolio()
        else:
            x[i] = list[i]
    return x

if params['liabilities']:
    plans = pd.DataFrame(l).join(pd.DataFrame(a), how='left')
    plans.columns = ['Liabilities', 'Portfolio']
    plans['Portfolio'] = nullPortfolios(plans['Portfolio'])
    plans = plans.apply(lambda x: Plan(val_date=config['valuation_date'], t=config['t'],
                                       liabilities=x.Liabilities, assets=x.Portfolio), axis=1)
    # set duration
    plans[0].liabilities.duration = config['liabilities']['duration']


config['n_simul'] = 10

#### FACTOR SIMULATION ####

if params['factors'] or params['curves']:
    cor             = pd.read_excel(config['file'], sheet_name='Cor')
    randoms         = pd.DataFrame(randCor(int(config['n_simul']), cor))
    randoms.columns = cor.columns


# SCENARIO BASE

loss = np.array([[0., 0.]] * config['n_simul'])

if params['liabilities']:
    PBO_base = plans[0].liabilities.PBO()
    NPV_base = plans[0].assets.NPV()
    insuran  = 0
    #### SCENARIO VALUATION

    for n in range(0, config['n_simul']):  # For simulation 'n'
        if params['curves']:
            for f in simulator_curves.index:  # For curves     'j'
                sim_curves[f].rates = simulator_curves[f].sim(random=randoms[f][n])
        if params['factors']:
            for f in simulator_factors.index:  # For factor     'j'
                sim_factor[f].factor[0] = simulator_factors[f].sim(random=randoms[f][n])
        loss[n] = [plans[0].assets.NPV(), plans[0].liabilities.PBO()]
        print(n)


#### LONGETIVIY ####

if not params['liabilities']:
    PBO_base = config['mortality_risk']['PBO']
    NPV_base = config['mortality_risk']['NPV']
    insuran  = config['mortality_risk']['Insurance']


BASE = NPV_base - PBO_base + insuran

LVar    = PBO_base * config['mortality_risk']['Sensitivity'] / config['mortality_risk']['Ext_life']
Sigma_p = LVar / norm.ppf(1 - config['mortality_risk']['mort_p'])


loss = pd.DataFrame(loss)
loss.columns = ['NPV', 'PBO']

if not params['liabilities']:
    loss.PBO = PBO_base
    loss.NPV = NPV_base

mean_assets      = loss.NPV.mean()
mean_liabilities = loss.PBO.mean()
mean_marketRisk  = mean_assets - mean_liabilities

loss['Market Risk'] = loss.NPV - loss.PBO
loss['M centered']  = loss['Market Risk'] - mean_marketRisk
loss['X']           = np.random.normal(size=config['n_simul'])

# Grand-Smith

def Grand_Smith(x, y):
    try:
        factor = sum(x * y) / sum(y ** 2)
    except ZeroDivisionError:
        print("Constant Market Risk -> Grand Smith does not apply")
        return x
    return x - y * factor


loss['X']          = Grand_Smith(loss['X'], loss['M centered'])
loss['Long Risk']  = loss['X'] * Sigma_p
loss['Total Risk'] = loss['Market Risk'] - loss['Long Risk'] - BASE + insuran

p = (1 - config['mkt_p']) * 100
per = list([int(np.percentile(loss['NPV'], p )),
            int(np.percentile(loss['PBO'], p )),
            int(np.percentile(loss['Market Risk'], p)),
            int(np.percentile(loss['Long Risk'], p)),
            int(np.percentile(loss['Market Risk'] - loss['Long Risk'], p)),
            int(np.percentile(loss['Total Risk'], p))])
print(per)