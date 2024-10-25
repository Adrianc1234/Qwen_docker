import SwiftUI

struct ContentView: View {
    @State private var inputText = ""
    @State private var predictionResult = ""

    let modelHandler = ModelHandler()

    var body: some View {
        VStack {
            Text("Interacción con el Paciente")
                .font(.title)

            TextField("Introduce tu texto aquí", text: $inputText)
                .padding()
                .textFieldStyle(RoundedBorderTextFieldStyle())

            Button("Generar Respuesta") {
                // Llamar a la función predict sin el argumento 'usingLength64'
                predictionResult = modelHandler.predict(inputText: inputText)
            }
            .padding()

            Text("Resultado: \(predictionResult)")
                .padding()
        }
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
