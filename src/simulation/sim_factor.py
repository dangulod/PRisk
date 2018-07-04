import numpy as np

def randCor(n_simul, M):
    u, s, v = np.linalg.svd(M)
    A = np.zeros((M.shape))
    np.fill_diagonal(A, np.sqrt(s))
    R = np.random.normal(0, 1, ( M.shape[1], n_simul))

    return np.dot(np.dot(u, A), R).transpose()

if __name__ == "__main__":
    # Simular factores a partir de una matriz de correlaciones

    import pandas as pd

    M = np.array([[ 1 , 0.2, 0.3,],
                  [0.2,   1, 0.1 ],
                  [0.3, 0.1,   1 ]])

    X = randCor(1000000, M)
    X = pd.DataFrame(X)
    print(X.corr())
