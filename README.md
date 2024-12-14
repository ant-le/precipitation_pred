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
I just chose some of the deadline dates for the 
aggregation of work arbitrarily. Feel free to
change this :)

|  Deadline  | Task                        | Assignee  | Status   |
| ---------- | --------------------------- | --------- | -------- |
| asap       | Create 100 files dataset    | Yeongshin | :heavy_check_mark: |
| 16.12.2024 | EDA and Processing          | all       |          |         
| 18.12.2024 | Combine EDA+Processing      | Anna      |          |
| 20.12.2024 | Setup Baseline Model        | Anton     |          |
| 30.12.2024 | Model Development           | all       |          | 
| 02.01.2025 | Combine Evaluations + Plots | Yeongshin |          | 
| 05.01.2025 | Report and Slides           | all       |          |
## Versioning
We will start with using Python **3.11.11** and 
potentially change the version based on compability
with the chosen models.

