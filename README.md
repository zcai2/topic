# Introduction
In order to better plan one's college course and eventual career options, it is essential to understand the topics being taught in each course. Every class tries to summarize its goals and outcomes with a course description, as well courses choose textbooks that are likely to meet those expectations. Students will often feel confused about the goal and outcome of a course because a course's description can either be too broad or too narrow for a beginner to comprehend. As a result, a certain percentage of students does not receive enough information to help them understand the course content as well as decide their future career direction. Planning future courses for a student is essential to help them attain their career goals. Unfortunately, assessing raw course information and aligning it to a career without any tools can prove to be difficult. In this paper, we will be applying an automated approach that enables us to find the hidden concepts and meanings within text-based documents, in particular course descriptions, textbook table of contents, summaries, and job listings. We did a comprehensive experiment with the course information from George Mason University (GMU). Our research also involves analysis of prerequisite chains in a GMU program of study. By mining and performing experiments on these datasets, topic modeling can discover the relationship between a course and connect the course to a suitable and desired job. We present our work as a user-facing web-based application (https://github.com/zcai2/topic). This software provides the overview for the book and course topic information as well as a job match feature.

## Supported Platforms

Sqlite3 (newest version)
Django (version 1.9).

## Usage
1: download porject
2: run python main.py
ps:
You might rename database.sql to database

## Project Feautre Description
Main Page of this Project
![image](https://user-images.githubusercontent.com/25554549/48011057-d5cb2780-e159-11e8-9012-2bc5d4365b4d.png)

Table of Contents (TOC): Input a book name or ISBN, you can view the topic ditribution of that book's TOC.
![image](https://user-images.githubusercontent.com/25554549/48011181-19be2c80-e15a-11e8-9ab2-4e194cc5c088.png)
Description: Input a book name or ISBN, you can view the topic ditribution of that book's description.
![image](https://user-images.githubusercontent.com/25554549/48011218-2b9fcf80-e15a-11e8-8e58-aa69fe3cdfce.png)
Class: Input a GMU course ID, CS310 in gmu is Data Strucuture
![image](https://user-images.githubusercontent.com/25554549/48011239-36f2fb00-e15a-11e8-9e78-c15a41e1d9ed.png)
Job: Input a GMU course ID, CS450 in gmu is Database Management and the matching job distribution for this couses shown as below:
![image](https://user-images.githubusercontent.com/25554549/48011311-60ac2200-e15a-11e8-9f26-2e3c0e16e09e.png)
Student also can view the job description.
![image](https://user-images.githubusercontent.com/25554549/48011271-4a9e6180-e15a-11e8-844f-2989e5a226be.png)
This figure shows the circle packet view of GMU courses.To allow users to visually see how much a topic takes of a particular course's required textbook, we provided an interactive circle packing graphic. Its allows users to click on the circles and zoom in to a particular course and see how much each of it's required textbooks take up of the related topics. For example, 
![image](https://user-images.githubusercontent.com/25554549/48136664-2f0e9480-e2db-11e8-92a1-5948e6890cd8.png)
This figure shows a zoomed in course circle. In the picture, the outer-most circle represents the course, and the two medium sized circles represent the two required books for the course. The colored circles represent the individual topics assigned to that course. For this course, it's two books are pretty relevant to the over all material and you can see how the topics are covered in pretty much equal size in both of the books.
![image](https://user-images.githubusercontent.com/25554549/48136720-55cccb00-e2db-11e8-8241-1170c2b40ac4.png)

By providing this interface we allow students and professors the opportunity to ensure that the required books match ups with the topics the course is aiming to cover. Or, if multiple books are required, it can ensure that the books cover enough distinct topics to justify their requirement.



## License and Authors

This work was done with Professor Huzefa Rangwala and undergraduate student Ameer Takaddein at George Mason University, funded by National Science Foundation.
Previous project Link:
https://github.com/atakieddin/Topics-Finder

If you have any questions, please contact me (zcai2@gmu.edu)

