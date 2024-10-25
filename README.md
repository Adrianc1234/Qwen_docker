
# Qwen App

This project is a Swift application that interacts with CoreML. Here are the steps to set up and run the project, along with details about a potential error and how to address it.

## Setup Instructions:

1. Clone the project repository:
   ```bash
   git clone <repository-url>
   ```
2. Open the project in Xcode:
   - Navigate to the folder where you cloned the project.
   - Open the `.xcodeproj` or `.xcworkspace` file in Xcode.
3. Ensure you have the `.mlpackage` in this folder `PatientInteractionApp/MLModel` file provided by me (This is a model format that I found because I could read or Render the ONNIX model with 200 files):
   - I will share the required `.mlpackage` file, which needs to be included in your project.
   - Drag and drop the `.mlpackage` file into your Xcode project.
   - Make sure the file is added to the correct target under **Build Phases > Copy Bundle Resources**.
4. Build and run the project:
   - Use **Product > Build** to compile the project.
   - Run the app using **Product > Run** in the iOS Simulator.

Link to download another models format:
[Folder](https://drive.google.com/drive/folders/1XVuec20mrfi-Uc1SnoAuucIVCjehY9DD?usp=sharing)

## Possible Error:

When running the app, you might encounter the following error if the `.mlpackage` is not included properly:

   ```
   Bundle Path: /Users/adriancarmonarodriguez/Library/Developer/CoreSimulator/Devices/47A806BA-E447-41CA-9BD5-369D2BE944BE/data/Containers/Bundle/Application/0CD05DE0-7FA6-4B0F-BC42-386414193632/PatientInteractionApp.app
   PatientInteractionApp/coreml_example.swift:25: Fatal error: No .mlpackage file found in the bundle.
   ```

This error occurs because the `.mlpackage` file required for CoreML processing is missing from the app bundle. Make sure the `.mlpackage` file is correctly included in the project and build target.

## Troubleshooting:

- Verify that the `.mlpackage` file is added to your Xcode project.
- Ensure the `.mlpackage` file is included in the "Copy Bundle Resources" build phase.
- Double-check the paths and references in the `coreml_example.swift` file to ensure the app is pointing to the `.mlpackage` file correctly.

## Alternate Approach:

If you're unable to run the project or prefer using your own CoreML model with multiple files, feel free to:
- Replace my `.mlpackage` file with your own model files.
- Create a new branch in the Git repository to experiment with different models and configurations.
  ```bash
  git checkout -b <new-branch-name>
  ```

You can modify the code and experiment with other models as needed. Ensure that any changes to CoreML models are properly reflected in the code by adjusting file paths and model configurations.
