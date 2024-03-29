import pandas as pd

from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from make_predictions import make_predictions
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold






class RamdomForestRegressorParameterSearcher(object):

    def train_and_score(self, training_set, final_features):

        """"Devuelve un array de tuplas, donde el primer elemento de cada tupla es el score para esa combinacion de hiper-parametros,
        se usa cross-validation"""    
        
        cantidadDeFeature=len(final_features)
        actual_data = training_set[final_features]
        labels = training_set["price_aprox_usd"]
        scores_actuales = []
        for x in range(5,40):
            print "Ahora probando con: "+str(x)+" min_samples_split"
            #cargo datos al modelo
            actual_data, labels = make_regression(n_features=cantidadDeFeature, n_informative=2,random_state=0, shuffle=False)
            ForestRegressor= RandomForestRegressor(n_estimators=10,max_depth=5, random_state=0,min_samples_split = x, min_samples_leaf = 15)
            scores = cross_val_score(ForestRegressor,X, Y, cv=20, scoring='neg_mean_squared_error', n_jobs = -1) 
            scores_actuales.append((scores.mean(),[x]))
        return scores_actuales

    def train_and_fit(self, training_set, final_features, hiperparameters):
        
        min_samples = hiperparameters[0]
        #cargo datos al modelo
        actual_data=training_set[final_features]
        labels=training_set["price_aprox_usd"]
        actual_data, labels = make_regression(n_features=cantidadDeFeature, n_informative=2,random_state=0, shuffle=False)
            ForestRegressor= RandomForestRegressor(n_estimators=10,max_depth=5, random_state=0,min_samples_split = min_samples, min_samples_leaf = 15)
        ForestRegressor.fit(actual_data, labels)    
         
        return  ForestRegressor



 
# define base model
def baseline_modelRedNueronal( int cantidadDeFeature):

    # create model
    model = Sequential()
    model.add(Dense(17, input_dim=cantidadDeFeature, init="normal", activation='relu'))#cantidad de entradas es el 4,inputdim
    #model.add(Dense(150, init='normal', activation='relu'))
    #model.add(Dense(150, init='normal', activation='relu'))
    model.add(Dense(6, init='normal', activation='relu'))
    model.add(Dense(1, init="normal"))#salida
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    
    return model



class RedNeuronalRegressorParameterSearcher(object):

    def train_and_score(self, training_set, final_features):

        """"Devuelve un array de tuplas, donde el primer elemento de cada tupla es el score para esa combinacion de hiper-parametros,
        se usa cross-validation"""  
        
        cantidadDeFeature=len(final_features)
        actual_data = training_set[final_features]
        labels = training_set["price_aprox_usd"]
        scores_actuales = []
        for x in range(5,40):
            print "Ahora probando con: "+str(x)+" epocas"
            # fix random seed for reproducibility
            seed = 7
            numpy.random.seed(seed)
            # evaluate model with standardized dataset
            RedKerasRegressor = KerasRegressor(build_fn=baseline_modelRedNueronal(cantidadDeFeature), nb_epoch=x, batch_size=32, verbose=2)
            kfold = KFold(n_splits=2, random_state=seed) 
            scores  = cross_val_score(estimator, actual_data, labels, cv=kfold,scoring='neg_mean_squared_error', n_jobs = -1)
           
            scores_actuales.append((scores.mean(),[x]))
        return scores_actuales

    
    def train_and_fit(self, training_set, final_features, hiperparameters):
        
        cantidadDeFeature=len(final_features)
        epoca = hiperparameters[0]
        # fix random seed for reproducibility
        seed = 7
        numpy.random.seed(seed)
        RedKerasRegressor = KerasRegressor(build_fn=baseline_model( cantidadDeFeature), nb_epoch=epoca, batch_size=32, verbose=2)
        RedKerasRegressor.fit(training_set[final_features], training_set["price_aprox_usd"])
        
        return RedKerasRegressor







class DecisionTreeRegressorParameterSearcher(object):

    def train_and_score(self, training_set, final_features):

        """"Devuelve un array de tuplas, donde el primer elemento de cada tupla es el score para esa combinacion de hiper-parametros,
        se usa cross-validation"""    

        actual_data = training_set[final_features]
        labels = training_set["price_aprox_usd"]
        scores_actuales = []
        for x in range(5,40):
            print "Ahora probando con: "+str(x)+" min_samples_split"
            regressor_tree = DecisionTreeRegressor(min_samples_split = x, min_samples_leaf = 15)
            scores = cross_val_score(regressor_tree, actual_data, labels, cv=20, scoring='neg_mean_squared_error', n_jobs = -1)
            scores_actuales.append((scores.mean(),[x]))
        return scores_actuales

    def train_and_fit(self, training_set, final_features, hiperparameters):
        
        min_samples = hiperparameters[0]
        regressor_tree = DecisionTreeRegressor(min_samples_split = min_samples, min_samples_leaf = min_samples)
        regressor_tree.fit(training_set[final_features], training_set["price_aprox_usd"])
        return regressor_tree

    

class KNeighborsRegressorParameterSearcher(object):
    
    def train_and_score(self, training_set, final_features):

        """"Devuelve un array de tuplas, donde el primer elemento de cada tupla es el score para esa combinacion de hiper-parametros,
        se usa cross-validation"""    

        actual_data = training_set[final_features]
        labels = training_set["price_aprox_usd"]
        scores_actuales = []
        for x in range(5,30):
            print "Ahora probando con: "+str(x)+" vecinos"
            knn = KNeighborsRegressor(n_neighbors= x)
            scores = cross_val_score(knn, actual_data, labels, cv=20, scoring='neg_mean_squared_error', n_jobs = -1)
            scores_actuales.append((scores.mean(),[x]))
        return scores_actuales

    def train_and_fit(self, training_set, final_features, hiperparameters):
        n = hiperparameters[0]
        knn = KNeighborsRegressor(n_neighbors = n)
        knn.fit(training_set[final_features], training_set["price_aprox_usd"])
        return knn


def find_best_model(training_set, model, final_features, cant_features):
#training_set: el set de training, completo
#model: el id del modelo a probar (ver arriba los ids implementados)
#final_features: una lista, puede ser vacia o contener inicialmente algun feature que se quiere que se tenga en cuenta
#cant_features: cantidad de features a probar, en un principio siempre es la cantidad de features - 4 (id y price no se prueban,
#rooms y surface_total_in_m2 ya los consideramos como necesarios)

#:return: modelo fitted al training set con los mejores parametros del modelo y mejores features encontrados
    scores_previos = []
    best_score = -float("inf") #Empiezo con un error infinito
    features_best_score = final_features
    best_hiper_parameters = []  
    agregar_nuevo_feature = False #Primera iteracion la hago con rooms y superficie total
    modelo_a_entrenar = implemented_models[model]
    while feature_actual < cant_features:   
        print "Inicio de una nueva iteracion"
        print "Best score actual: "+str(best_score)+", hasta ahora las cols son: "+str(features_best_score)+" y los mejores hiper-parametros son: "+",".join(best_hiper_parameters)
        if agregar_nuevo_feature:            
            final_features.append(features[feature_actual])

        scores_con_features_actuales = modelo_a_entrenar.train_and_score(training_set, final_features)
        improved = False
        for s in scores_con_features_actuales:
            if s[0] > best_score: #Hay que MAXIMIZAR el error cuadratico medio negativo
                 best_score = s[0]
                 features_best_score = list(final_features)
                 best_hiper_parameters = s[1]
                 improved = True
        if not(improved):
            final_features.remove(features[feature_actual])
      
        feature_actual += 1
        scores_previos.append(scores_actuales)
       
        agregar_nuevo_feature = True #Agrego nuevo feature a partir de la segunda iteracion
        print "Fin de la ultima iteracion"

    print "Best score actual: "+str(best_score)+", hasta ahora las cols son: "+str(features_best_score)+" y los mejores hiper-parametros son: "+",".join(best_hiper_parameters)
    print "Entrenando el mejor modelo hallado..."
    best_model = modelo_a_entrenar.train_and_fit(training_set, features_best_score, best_hiper_parameters)
    return best_model,features_best_score

modes = ["train_model","find_best_model"]
implemented_models = {"knn":KNeighborsRegressorParameterSearcher(),"decisiontree":  DecisionTreeRegressorParameterSearcher(),"redNeuronal":RedNeuronalRegressorParameterSearcher()}

def main():
    
    if (len(sys.argv) < 6) or (len(sys.argv) > 7):
        print len(sys.argv)
        print ""
        print "ERROR! la forma de usar es <find_best_model <regressorModelId> <training_set_file> <testing_set_file> <save_file_name>"
        print ""
        print "o: <train_model <regressorModelId> <training_set_file> <testing_set_file> <features> <save_file_name>"
        print ""
        print "Ejemplo si se quiere buscar los mejores hiperparametros para KNN y guardar el resultado del test set ingresar:"
        print ""
        print "find_best_model KNN <nombre del archivo del training set> <nombre del archivo del test set> <nombre archivo a guardar los resultados>"
        print ""
        print "Si se quiere probar KNN con determinadas columnas, buscando solamente el mejor k, ingresar: "
        print ""
        print "train_model KNN <nombre del archivo del training set> <nombre del archivo del test set> <nombre arch donde guardar results>"
        print ""
        print "@@@@@LOS ARCHIVOS TRAINING Y TESTING YA TIENEN QUE ESTAR PREPROCESADOS, SIN NINGUN NULL, Y COMPRIMIDOS@@@@@"
        print "@@@@@Si no se indica, debugging = True y save_model = False@@@@@@@"
        print "@@@@@Ingresar los features en un formato tipo f1,f2,f3,...,fn@@@@@@@"
        return

    else:
        
        mode = sys.argv[1]
        if mode.lower() not in modes:

            print "ERROR! los modos son: train_model o find_best_model"
            return

        if mode.lower() == "train_model" and len(sys.argv) != 7:
            print "Faltan argumentos para train_model"
            return

        if mode.lower() == "find_best_model" and len(sys.argv) != 6:
            print "Faltan arguementos para find_best_model"
            return

        model = sys.argv[2]
        if model.lower() not in implemented_models:

            print "No se ha implementado aun el modelo: "+model
            print "Modelos disponibles: "+str(",".join(implemented_models))
            return

        training_set_path = sys.argv[3]
        #try:    
        training_set = pd.read_csv(training_set_path)
        #except IOError:

         #   print "No se puede abrir el archivo de training. O ya se encuentra en uso por otro programa, o se indico un path incorrecto"
         #   return

        testing_set_path = sys.argv[4]
        #try:
        testing_set = pd.read_csv(testing_set_path)
        #except IOError:

         #   print "No se puede abrir el archivo de testing. O ya se encuentra en uso por otro programa, o se indico un path incorrecto"
         #   return

    file_name = sys.argv[len(sys.argv) - 1]
        
    if mode.lower() == "find_best_model":

        
        #features a probar
        features = list(training_set.columns)
        features.remove("id")
        features.remove("price_aprox_usd")
        features.remove("rooms")
        features.remove("surface_total_in_m2")
        #Cantidad de features a probar con forward selection:
        cant_features = len(features) - 4 #No tengo en cuenta Id y price_aprox_usd (id no es un feature, price es lo que quiero predecir (target), ni rooms ni superficie total (estos dos features no se descartan nunca)
        feature_actual = 0
        final_features = ["rooms","surface_total_in_m2"] #fija que estan estos dos. 
        info_entrenamiento = find_best_model(training_set, model, final_features, cant_features)

        best_model = info_entrenamiento[0]
        best_features = info_entrenamiento[1]
        make_predictions(best_model, test_set, best_features, file_name)
        return

    elif mode.lower() == "train_model":

        #ESTO MOVERLO, DEBERIA RECIBIR YA ASI AL ARCHIVO
        testing_set.fillna(training_set.mean(), inplace = True) 

        final_features = sys.argv[5].split(",")
        print final_features
        #Con estos features busco los mejores parametros
        model_to_train = implemented_models[model]
        scores_con_features_actuales = model_to_train.train_and_score(training_set, final_features)
        best_score = -float("inf")
        best_hiper_parameters = []
        for s in scores_con_features_actuales:
            if s[0] > best_score: #Hay que MAXIMIZAR el error cuadratico medio negativo
                 best_score = s[0]
                 best_hiper_parameters = s[1]

        best_model = model_to_train.train_and_fit(training_set, final_features, best_hiper_parameters)
        
        make_predictions(best_model, testing_set, final_features, file_name)


main()
