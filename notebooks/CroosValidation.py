    #   IMPORTS 
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tsxv.splitTrainValTest import split_train_val_test_groupKFold
import time
from itertools import product

    #   CONFIGURACIONES INICIALES
btc = pd.read_csv(r"C:\Users\Hp\MACHINE\MINI_PRY_2\data\BTC_all.csv")
btc = btc.sort_values(by='Date') 

WINDOW_SIZES = [7, 14, 21, 28]
#WINDOW_SIZES = [7]
RANDOM_STATE = 42

def train_and_predict_mlp(X_train, y_train, X_val, params):
    model = MLPRegressor(
        hidden_layer_sizes=params['hidden_layer_sizes'],
        activation='relu',
        solver='adam',
        alpha=params['alpha'],
        learning_rate='constant',
        max_iter=1000,
        early_stopping=True,
        validation_fraction=0.1,
        random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)
    # Hacer predicciones
    y_val_pred = model.predict(X_val)
    return y_val_pred, model


def calculate_metrics(y_true, y_pred, y_scaler):
    if y_scaler is not None:
        y_true = y_scaler.inverse_transform(y_true)
        y_pred = y_scaler.inverse_transform(y_pred)

    metrics = {'mae': [], 'rmse': [], 'smape': []}

    for day in range(7):
        y_true_day = y_true[:, day]
        y_pred_day = y_pred[:, day]

        mae = mean_absolute_error(y_true_day, y_pred_day)
        rmse = np.sqrt(mean_squared_error(y_true_day, y_pred_day))

        # Evitar división por cero
        mask = y_true_day != 0
        if mask.sum() > 0:
            smape = 100 * np.mean(2 * np.abs(y_pred_day - y_true_day) / (np.abs(y_true_day) + np.abs(y_pred_day)))
        else:
            smape = np.nan

        metrics['mae'].append(mae)
        metrics['rmse'].append(rmse)
        metrics['smape'].append(smape)

    metrics['avg_mae'] = np.nanmean(metrics['mae'])
    metrics['avg_rmse'] = np.nanmean(metrics['rmse'])
    metrics['avg_smape'] = np.nanmean(metrics['smape'])
    
    return metrics



# INICIO
param_grid = {
    'hidden_layer_sizes': [(64, 32), (100, 50),],
    'alpha': [ 0.0001, 0.001, 0.01, 0.1],
}
keys = list(param_grid.keys())
combinaciones = [dict(zip(keys, values)) for values in product(*param_grid.values())]

results = {}
global_best = {
    'window_size': None,
    'params': None,
    'rmse': float('inf'),
    'metrics': None
}

# Iterar por ventana
for window_size in WINDOW_SIZES:
    print(f"\n{'='*60}")
    print(f"=== Procesando ventana de {window_size} días === \n Se usa un lag de {window_size} días")

    best_config = None
    best_rmse = float('inf')

    # Parametros
    timeSeries = btc[f'Volatil_D{window_size}']
    numInputs = window_size # Máximo de lags a usar (28 días)
    numOutputs = 7
    numJumps = 1 # Salto de ventanas (1 día)
    print(f"Parámetros: numInputs={numInputs}, numOutputs={numOutputs}, numJumps={numJumps}")
    
    # Split
    X_t, Y_t, X_v, Y_v, X_st, Y_st = split_train_val_test_groupKFold(timeSeries, numInputs, numOutputs, numJumps)
    print(f" Numero de folds generados", len(X_t))
    

    i=1
    w_time = time.time()

    for config in combinaciones:
        #print(f"=== Procesando la combinación {i} ===")
        
        fold_results = []
        rmse_acumulado = []
        for fold in range (len(X_t)):

            # Dividir datos
            X_train, X_val, X_test = X_t[fold], X_v[fold], X_st[fold]
            Y_train, Y_val, Y_test = Y_t[fold], Y_v[fold], Y_st[fold]
            
            X_Scaler = StandardScaler()
            Y_Scaler = StandardScaler()

            X_train_S = X_Scaler.fit_transform(X_train)
            X_val_S = X_Scaler.transform(X_val)
            X_test_S = X_Scaler.transform(X_test)

            Y_train_S = Y_Scaler.fit_transform(Y_train)
            Y_val_S = Y_Scaler.transform(Y_val)
            Y_test_S = Y_Scaler.transform(Y_test)

            y_val_pred, model = train_and_predict_mlp(
                X_train_S, Y_train_S, X_val_S, config
            )

            val_metrics = calculate_metrics(Y_val_S, y_val_pred, Y_Scaler)
            rmse_acumulado.append(val_metrics['avg_rmse'])

            fold_results.append({
                'fold': fold,
                'model': model,
                'params': config,
                'metrics': val_metrics,
            })
        
        # ===== Comparación dentro de la configuracion  =====
        rmse_promedio = np.mean(rmse_acumulado)
        metrics_summary = {
            'avg_mae': np.mean([f['metrics']['avg_mae'] for f in fold_results]),
            'avg_rmse': np.mean([f['metrics']['avg_rmse'] for f in fold_results]),
            'avg_smape': np.mean([f['metrics']['avg_smape'] for f in fold_results])
        }

        if rmse_promedio < best_rmse:
            best_rmse = rmse_promedio
            best_config = config
            best_metrics_summary = metrics_summary

        i+=1

    fin_ventana = time.time() - w_time

    results[window_size] = {
        'best_params': best_config,
        'metrics_summary': best_metrics_summary,
        'time': fin_ventana
    }
    # ===== Comparación global =====
    if best_rmse < global_best['rmse']:
        global_best['window_size'] = window_size
        global_best['params'] = best_config
        global_best['rmse'] = best_rmse
        global_best['metrics'] = best_metrics_summary
        global_best['time'] = fin_ventana


print("\n📊 Resultados por ventana:")
for w, res in results.items():
    print(f"\n=== Ventana {w} días ===")
    print(f"  ➤ Mejores hiperparámetros: {res['best_params']}")
    print(f"  ➤ Promedio en folds: ")
    print(f"       MAE  = {res['metrics_summary']['avg_mae']:.4f}")
    print(f"       RMSE = {res['metrics_summary']['avg_rmse']:.4f}")
    print(f"       SMAPE = {res['metrics_summary']['avg_smape']:.2f}%")
    print(f"  ➤ Tiempo total: {res['time']:.2f} segundos")

print("\n🏆 Mejor resultado global:")
print(f" Ventana: {global_best['window_size']} días")
print(f" Hiperparámetros: {global_best['params']}")
print(f" Métricas promedio en folds:")
print(f"    MAE  = {global_best['metrics']['avg_mae']:.4f}")
print(f"    RMSE = {global_best['metrics']['avg_rmse']:.4f}")
print(f"    SMAPE = {global_best['metrics']['avg_smape']:.2f}%")
print(f" Tiempo: {global_best['time']:.2f} segundos")
