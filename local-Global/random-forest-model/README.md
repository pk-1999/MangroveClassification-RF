# Random Forest Multi-Classification Model

This project implements a random forest multi-classification model using the GMD_v1.csv dataset. The model predicts the 'landcover' class based on the features 'red', 'nir', 'swir1', and 'swir2'.

## Project Structure

The project has the following structure:

```
random-forest-model
├── src
│   ├── main.py
│   ├── model
│   │   └── random_forest.py
│   └── data
│       └── GMD_v1.csv
├── requirements.txt
└── README.md
```

- `src/main.py`: This file is the entry point of the application. It reads the 'GMD_v1.csv' data file and builds a random forest multi-classification model using the features 'red', 'nir', 'swir1', and 'swir2' to predict the 'landcover' class.

- `src/model/random_forest.py`: This file exports a class `RandomForestModel` which implements the random forest multi-classification model. It provides methods to train the model, make predictions, and evaluate the model's performance.

- `src/data/GMD_v1.csv`: This file contains the input data in CSV format. It includes the features 'red', 'nir', 'swir1', 'swir2', and the target variable 'landcover'.

- `requirements.txt`: This file lists the dependencies required for the project. It specifies the Python packages and their versions needed to run the code.

## Getting Started

To set up and run the random forest multi-classification model, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/random-forest-model.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main.py file:

   ```bash
   python src/main.py
   ```

   This will train the random forest model using the GMD_v1.csv dataset and make predictions for the 'landcover' class.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

Feel free to contribute to the project by opening a pull request or submitting an issue.