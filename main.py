import mysql.connector
import numpy as np
from scipy import stats
import statsmodels.api as sm
import pandas as pd
from tabulate import tabulate as tblt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Collegamento al DB
mydb = mysql.connector.connect(
  host="localhost",
  user="cpsm",
  password="Headband2+Designate+Subscribe+Graceful+Canary",
  database="BloodGroup"
)



# Ottenere i dati dal DB

def get_array(column: str, continent = None) -> np.array:
    try:
        trasaction = mydb.cursor()

        if continent == None:   
            trasaction.execute(f"Select `{column}` from country")
        else:
            trasaction.execute(f"Select `{column}` from country where continent = '{continent}'")
        
        return np.array([float(y) for x in trasaction.fetchall() for y in x ])
    finally:
        trasaction.close()



# Classificazione dei dati

def grouping_array(array: np.array) -> np.array:
    group = []
    s_a = round(
        ((np.mean(np.absolute(array - np.mean(array)))) / 2), 
        3)

    print(s_a)
    for x in array:
        group.append(s_a * round((x / s_a), 0))

    return np.array(group)



# Creazione della tabella di Frequenza

def frequency_table(array: np.array, grouping = True) -> dict:
    if grouping:
        array = grouping_array(array)

    v, f = np.unique(array, return_counts = True)
    p = [(round(i/len(array), 3)) for i in f]
    
    F, P, ante = [], [], 0.0
    for i in f:
        F.append(i + ante)
        P.append(round(((i+ante) / len(array)), 3))
        ante += i
    
    info = {
        'v_i': v,
        'f_i': f,
        'p_i': p,
        'F_i': F,
        'P_i': P
    }
    print(tblt(info, headers = 'keys', showindex = range(1, len(v)+1), tablefmt = 'grid'))
    
    return info



# Indice di Posizione

def position_indexs(array: np.array) -> None:
    info = {
        'Media': [round(np.mean(array), 2)],
        'Mediana': [np.median(array)],
        'Moda': stats.mode(list(array), keepdims = True)[0]
    }

    print(tblt(info, headers = 'keys', tablefmt = 'grid'))
    pass



# Indice di Variabilità

def var_indexs(array: np.array) -> None:
    info = {
        's^2': [np.var(array, ddof = 1)],                           # Varianza Campionaria
        's': [np.std(array, ddof = 1)],                             # Deviazione standard
        's_a': [np.mean(np.absolute(array - np.mean(array)))],      # Scarto Medio Assoluto
        'w': [np.max(array) - np.min(array)]                        # Ampiezza di Campo di variazione
    }
    
    print(tblt(info, headers = 'keys', tablefmt = 'grid'))
    pass



# Indice di Forma

def shape_indexs(array: np.array) -> None:
    info = {
        'Asimmetria': [stats.skew(array)],
        'Curtosi': [stats.kurtosis(array, fisher = False)]
    }

    print(tblt(info, headers = 'keys', tablefmt = 'grid'))
    pass



# Tabella dei Quartili

def quantil_indexs(array: np.array) -> None:
    info = {
        '1 Quartile': [np.quantile(array, 0.25)],
        '2 Quartile': [np.quantile(array, 0.5)],
        '3 Quartile': [np.quantile(array, 0.75)]
    }

    print(tblt(info, headers = 'keys', tablefmt = 'grid'))
    pass



# Coefficiente di Correlazione

def corcorrelation_coeff(x: np.array, y: np.array) -> None:
    info = {
        'Coefficiente di correlazione': [round(stats.pearsonr(x, y)[0], 4)]
    }

    print(tblt(info, headers = 'keys', tablefmt = 'grid'))
    pass



# Creazione dei Box Plot

def create_box_plot(title: str, *args: list[str, np.array]) -> None:
    fig = go.Figure()

    for arg in args:
        fig.add_trace(
            go.Box(
                y = arg[1], 
                name = arg[0]
            )
        )
    

    fig.update_layout(title_text = title)
    fig.show()
    pass


# Creazione dei Diagrammi a Dispersione con Regressione

def create_scatter(title: str, *args: list[str, np.array, np.array]) -> None:
    row = 2 if len(args) > 2 else 1
    col = int(len(args) / row)

    fig = make_subplots(rows = row, cols = col)
    
    for i in range(row):    
        for j in range(col):
            df = pd.DataFrame({
                'X': args[i+(j+i)][1], 
                'Y': args[i+(j+i)][2]
                })

            # Regressione lineare
            df['bestfit'] = sm.OLS(
                    df['Y'],
                    sm.add_constant(df['X'])
                ).fit().fittedvalues
            
            # Diagramma a Dispersione
            fig.append_trace(
                go.Scatter(
                    name = f'{args[j+(i*int(len(args)/row))][0]}', 
                    x = df['X'], 
                    y = df['Y'].values, 
                    mode='markers'
                ), 
                i+1, 
                j+1
            )
            
            # Linea di Regressione lineare
            fig.append_trace(
                go.Scatter(
                    name = f'regrex line {args[ j + (i * int(len(args) / row))][0]}', 
                    x = args[j+(i*int(len(args) / row))][1], 
                    y = df['bestfit'], 
                    mode = 'lines'
                ), 
                i + 1, 
                j + 1
             )


    fig.update_layout(title_text = title, xaxis_title = "Rh +", yaxis_title = "Rh -")
    fig.show()    
    pass


# Creazione degli Istogrammi

def create_hist_graph(title: str, *args: list[str, np.array]) -> None:
    row = 2 if len(args) > 2 else 1
    col = int(len(args) / row)

    fig = make_subplots(rows = row, cols = col)

    # Creazione dei vari diagrammi
    hists = [
        go.Histogram(
            x = arg[1], 
            name = arg[0], 
            xbins = dict(
                size = round( ((np.mean(np.absolute(arg[1] - np.mean(arg[1])))) / 2), 3)     # Ampiezza delle aste
            )
        ) 
        for arg in args]

    for i in range(row):
        for j in range(col):
            fig.append_trace(hists[(i * int(len(args) / row)) + j], i + 1, j + 1)


    fig.update_layout(title_text = title)
    fig.show()
    pass


if __name__ == '__main__':

    # Test Enviroment

    pass
    
    