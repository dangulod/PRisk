import sys

import pandas as pd
import numpy as np
from scipy.stats import norm

from src.curves.curve import Curve, get_curve, copy_curve

from src.dates.date import Date, Days, Years

from src.assets.products import Portfolio
import src.assets.products as pricers

from src.liabilities.liabilities import Liabilities

from src.Plan.Plan import Plan

from src.simulation.sim_factor import randCor
from src.simulation.factor import Factor, copy_factor, get_factor
import src.simulation.models as models

if (len(sys.argv) == 1): sys.argv = sys.argv + ['Germany/DE_config.xlsx']


print('Reading file', sys.argv[1])

## Reading Main
data = pd.read_excel(sys.argv[1], sheet_name='main')

data.valuation_date = data.valuation_date.apply(lambda x: Date(x.day, x.month, x.year))
data.t              = data.t.apply(lambda x: eval(x))

config = data.to_dict(orient='records')[0]
## Reading Liabilities

liabilities = pd.read_excel(sys.argv[1], sheet_name='liabilities').to_dict(orient='records')[0]
config['liabilities'] = liabilities

mortality_risk = pd.read_excel(sys.argv[1], sheet_name='mortality_risk').to_dict(orient='records')[0]
config['mortality_risk'] = mortality_risk

imp_factors = pd.read_excel(sys.argv[1], sheet_name='factors')
factors = {}

for f in imp_factors.index:
    model = imp_factors.model[f]

    curve = imp_factors.curve[f]
    vol = imp_factors.vol[f]
    flag = bool(imp_factors.flag[f])

    params = {'curve' : curve,
              'vol'   : vol,
              'flag'   : flag}

    factors[f] = {'model'  : model,
                  'params' : params}
config['factors'] = factors

imp_curves = pd.read_excel(sys.argv[1], sheet_name='curves')
curves = {}

for c in imp_curves.index:
    model = imp_curves.model[c]

    MRV = imp_curves.MRV[c]
    MRS = imp_curves.MRS[c]
    vol = imp_curves.vol[c]
    flag = bool(imp_curves.flag[c])

    params = {'MRV' : MRV,
              'MRS' : MRS,
              'vol' : vol,
              'flag'   : flag}

    curves[c] = {'model'  : model,
                 'params' : params}
config['curves'] = curves


######################################################

np.random.seed(config['seed'])

##### LOAD CURVES ####

curves = pd.read_excel(config['file'], sheet_name="Curves")
curves.Tenor = curves.Tenor.apply(lambda x: config['valuation_date'] + Days(x))

curves = curves.groupby('Name').\
    apply(lambda x: Curve(name=str(x.Name.unique()[0]),
                          dates=x.Tenor.tolist(),
                          rates=x.Rate.tolist()))

#### LOAD PORTFOLIO ####

a = pd.read_excel(config['file'], sheet_name="Assets")

a[a.select_dtypes(include=['datetime']).columns] = \
    a[a.select_dtypes(include=['datetime']).columns].\
    applymap(lambda x: Date(x.day, x.month, x.year))


for c in curves.index:
    pos = np.where((a.curve_irr == c) * [1] == 1)[0].tolist()
    if pos:
        zzz = int(max(a.matDate[pos]).year())
    else:
        zzz = int(config['valuation_date'].year())
    zzz = max(zzz, curves[c].dates[-1].year()+1)
    reqyears = int(max(zzz - config['valuation_date'].year(), int(config['liabilities']['duration'] / 365) + 1))
    curves[c].extrapolationCDS(rf=config['rf'], RR=config['RR'], val_date=config['valuation_date'],
                                       reqyears=reqyears)


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
a['curve_irr'] = a['curve_irr'].apply(lambda x: get_curve(x, sim_curves))
a['curve_spread'] = a['curve_spread'].apply(lambda x: get_curve(x, sim_curves))
a['factor'] = a['factor'].apply(lambda x: get_factor(x, sim_factor))

a['args'] = a.drop(['Pais', 'Plan', 'pricer'], axis=1).\
    apply(lambda x: x.to_dict(), axis=1)

a = a[['Pais', 'Plan', 'pricer', 'args']]

a["Portfolio"] = a.apply(lambda x: getattr(pricers, x['pricer'])(val_date=config['valuation_date'],
                                                                 t=config['t'],
                                                                 **x['args']), axis=1)

a = a[['Pais', 'Plan', 'Portfolio']].\
    groupby(['Pais', 'Plan']).\
    agg(Portfolio.create_portfolio).Portfolio


#### LOAD LIABILITIES ####

l = pd.read_excel(config['file'], sheet_name="Liabilities")

l[l.select_dtypes(include=['datetime']).columns] = \
    l[l.select_dtypes(include=['datetime']).columns]. \
        applymap(lambda x: Date(x.day, x.month, x.year))

l = l.groupby(['Pais', 'Plan']). \
    apply(lambda x: Liabilities(val_date=config['valuation_date'],
                                dates=x.FechaCF.tolist(),
                                flows=x.CF.tolist(),
                                curve_irr=get_curve(config['liabilities']['curve_irr'], sim_curves),
                                curve_spread=get_curve(config['liabilities']['curve_spread'], sim_curves),
                                curve_inf=get_curve(config['liabilities']['curve_inf'], sim_curves)))


#### CREATE PLANS ###

plans = pd.DataFrame(l).join(pd.DataFrame(a), how='left')

plans.columns = ['Liabilities', 'Portfolio']


def nullPortfolios(list):
    x = [0] * len(list)
    for i in range(0, len(list)):
        if pd.isna(list[i]):
            x[i] = Portfolio()
        else:
            x[i] = list[i]
    return x

plans['Portfolio'] = nullPortfolios(plans['Portfolio'])

plans = plans.apply(lambda x: Plan(val_date=config['valuation_date'], t=config['t'],
                                   liabilities=x.Liabilities, assets=x.Portfolio), axis=1)


#### FACTOR SIMULATION ####

cor = pd.read_excel(config['file'], sheet_name='Cor')

randoms = pd.DataFrame(randCor(int(config['n_simul']), cor))
randoms.columns = cor.columns


# Set duration

plans[0].liabilities.duration = config['liabilities']['duration']


# SCENARIO BASE

PBO_base = plans[0].liabilities.PBO()
NPV_base = plans[0].assets.NPV()

BASE = NPV_base - PBO_base

#### LONGETIVIY ####

LVar    = plans[0].liabilities.PBO() * config['mortality_risk']['Sensitivity']
Sigma_p = LVar / norm.ppf(1 - config['percentile'])


#### SCENARIO VALUATION

from datetime import *

start = datetime.today()

loss = np.array([[0., 0.]] * config['n_simul'])

for n in range(0, config['n_simul']):                              # For simulation 'n'
    for f in simulator_curves.index:                               # For curves     'j'
        sim_curves[f].rates = simulator_curves[f].sim(random=randoms[f][n])
    for f in simulator_factors.index:                              # For factor     'j'
        sim_factor[f].factor[0] = simulator_factors[f].sim(random=randoms[f][n])
    loss[n] = [plans[0].assets.NPV(), plans[0].liabilities.PBO()]
    print(n)
stop = datetime.today()

loss = pd.DataFrame(loss)

loss.columns = ['NPV', 'PBO']

mean_assets      = loss.NPV.mean()
mean_liabilities = loss.PBO.mean()
mean_marketRisk  = mean_assets - mean_liabilities

loss['Market Risk'] = loss.NPV - loss.PBO
loss['M centered']  = loss['Market Risk'] - mean_marketRisk
loss['X']           = np.random.normal(size=config['n_simul'])

# Grand-Smith

def Grand_Smith(x, y):
    factor = sum(x * y) / sum(y ** 2)
    return x - y * factor


loss['X']          = Grand_Smith(loss['X'], loss['M centered'])
loss['Long Risk']  = loss['X'] * Sigma_p
loss['Total Risk'] = loss['Market Risk'] - loss['Long Risk'] - BASE

p =(1 - config['percentile']) *100
per = list([int(np.percentile(loss['NPV'], p )),
            int(np.percentile(loss['PBO'], p )),
            int(np.percentile(loss['Market Risk'], p)),
            int(np.percentile(loss['Long Risk'], p)),
            int(np.percentile(loss['Market Risk'] - loss['Long Risk'], p)),
            int(np.percentile(loss['Total Risk'], p))])
print(per)