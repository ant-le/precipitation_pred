# Precipitation Prediction 

## Usage
To get started with all the dependencies, run 
```sh
pip3 install -r requirements.txt
```

To get the dataset in a script of notebook run:
```py
from get_data import create_df
data = create_df()
```
The script will search for a data folder and if it 
does not exists it will download the relevant data 
and randomly sample 100 files from the dataset into
a folder called `data`. In case you have a different
folder name your can provide the name as an 
argument to the function.

Secondly, the script will create a combined dataset
out of the 100 files and index it by the date and 
index of the file.


## Timetable

|  Deadline  | Task                        | Assignee  | Status             |
| ---------- | --------------------------- | --------- | ------------------ |
| asap       | Create 100 files dataset    | Yeongshin | :heavy_check_mark: |
| 16.12.2024 | EDA and Processing          | all       |                    |
| 18.12.2024 | Combine EDA+Processing      | Anna      |                    |
| 20.12.2024 | Setup Baseline Model        | Anton     |                    |
| 30.12.2024 | Model Development           | all       |                    | 
| 02.01.2025 | Combine Evaluations + Plots | Yeongshin |                    | 
| 05.01.2025 | Report and Slides           | all       |                    |

## Models
We decided one the following models and will take the `RMSE` and the `MSE`:
1. **Linear Regression** as a Baseline Model
2. **LSTM**
3. **Hierarchical Model** (Bayesian Models also capturing seasonalities)
4. Ensembe of **Regression Trees** for each region

In case some of the given approaches will not work, we will opt for [SARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average), which are known to perform well on time-series data with seasonal dependencies.



## Versioning
We will start with using Python **3.11.11** and 
potentially change the version based on compability
with the chosen models.

