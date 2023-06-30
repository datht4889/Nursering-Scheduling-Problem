# 

## Description

* **Input**: N, D, a, b respectively represent number of Nurse, Day, lower and upper bound of number of nurse in a shift.
* **Constraints**: Each day, each nurse works at most one shift.
A nurse would not work if she worked on the night shift the day before.
Each nurse has a list of rest days and does not work on those days.
Each shift has at least alpha nurses and at most beta nurses.
* **Output**: The optimal schedule for N nurses and
The maximum number of night shifts worked by a nurse.



## Getting Started

### Dependencies
* Python
* Google OR-Tools

### Installing
1. Download this project as zip and extract it.
2. Install **Google OR-Tools** .

    * Windows installation
    ```
    python -m pip install --upgrade --user ortools
    ```

    * Mac installation
    ```
    python3 -m pip install --upgrade --user ortools
    ```


### Executing program

* **backtracking.py** solves Nurse Rostering Problem by using Backtracking Algorithm.
* **CP.py** solves Nurse Rostering Problem with Constraint Programming based on OR-Tools.
* **localsearch.py** solves Nurse Rostering Problem with Local Search and meta heuristic strategies.
* **MIP.py** solves Nurse Rostering Problem by using Mixed Integer Programming. 
* **shift.csv** and **time.csv** are files we use to analyse and compare among algorithms in our report.

## Contributors
* Hoàng Thành Đạt: dat.ht214889@sis.hust.edu.vn
* Nguyễn Hoàng Anh: anh.nh214946@sis.hust.edu.vn
* Đặng Minh Đức: duc.dm214956@sis.hust.edu.vn
