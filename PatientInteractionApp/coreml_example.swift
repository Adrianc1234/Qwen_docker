import CoreML

class ModelHandler {
    var model: MLModel?   // El modelo cargado desde el .mlpackage
    
    init() {
        loadModel()  // Cargar el modelo
    }

    func loadModel() {
        // Obtén la ruta del bundle y la imprimimos para verificar
        let bundlePath = Bundle.main.bundlePath
        print("Bundle Path: \(bundlePath)")
        
        // Cambiamos para buscar el archivo en la carpeta "MLModel"
        if let modelURL = Bundle.main.url(forResource: "Qwen_2_1_5B_6Bits_MF", withExtension: "mlpackage", subdirectory: "MLModel") {
            print("Ruta del modelo encontrada: \(modelURL)")
            do {
                // Cargar el modelo completo desde la carpeta especificada
                model = try MLModel(contentsOf: modelURL)
            } catch {
                fatalError("Error al cargar el modelo: \(error.localizedDescription)")
            }
        } else {
            fatalError("No se pudo encontrar el archivo .mlpackage en el bundle.")
        }
    }

    // Función para predecir usando el modelo cargado
    func predict(inputText: String) -> String {
        guard let model = model else {
            return "Error: Modelo no cargado correctamente."
        }

        // Aquí debes tokenizar el texto de entrada
        let inputTokens: [Int32] = tokenize(inputText)
        
        // Aquí está la estructura de input para el modelo, que requiere input_ids y query_pos1
        let inputFeatures: [String: Any] = [
            "input_ids": inputTokens,
            "query_pos1": [Int32(0)] // Similar al script de Python
        ]

        do {
            // Predecir usando las características proporcionadas
            let prediction = try model.prediction(from: MLDictionaryFeatureProvider(dictionary: inputFeatures))
            
            // Procesar los logits o la salida similar a cómo se maneja en el script de Python
            return processPrediction(prediction: prediction)
        } catch {
            return "Error en la predicción: \(error.localizedDescription)"
        }
    }

    func tokenize(_ text: String) -> [Int32] {
        // Implementa la lógica para convertir el texto en tokens (usa el tokenizador de Hugging Face si es posible)
        return [101, 102, 103]  // Placeholder: Cambia esto por tu tokenización real
    }

    func processPrediction(prediction: MLFeatureProvider) -> String {
        // Procesar los logits para generar el texto de salida
        return "Texto generado (implementar)"
    }
}
