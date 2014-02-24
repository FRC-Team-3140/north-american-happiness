# Overview

One table, choices, will contain a mapping of (int id) to (varchar choice), which another table, teams, will reference. teams will have columns of (varchar teamnumber), (foreignkey[question] questionid), (foreignkey[choice] choice). Then there will be a table, questions, which has (int id) and (varchar question).

## Database

    CREATE DATABASE IF NOT EXISTS scout;

## Table: choices

    CREATE TABLE IF NOT EXISTS scout.choices (
        id INTEGER NOT NULL AUTO_INCREMENT,
        choice VARCHAR(1024),
        PRIMARY KEY (id)
    );

## Table: questions

    CREATE TABLE IF NOT EXISTS scout.questions (
        id INTEGER NOT NULL AUTO_INCREMENT,
        question VARCHAR(1024),
        PRIMARY KEY (id)
    );

## Table: teams

    CREATE TABLE IF NOT EXISTS scout.teams (
        id INTEGER NOT NULL AUTO_INCREMENT,
        teamnumber VARCHAR(8),
        question INTEGER REFERENCES scout.questions,
        choice INTEGER REFERENCES scout.choices,
        PRIMARY KEY (id)
    );

## Using the tables

    INSERT INTO scout.questions VALUES (1, "Programming language used"); -- id 1
    INSERT INTO scout.choices VALUES (1, "LabVIEW"); -- id 1
    INSERT INTO scout.choices VALUES (2, "Java"); -- id 2

    INSERT INTO scout.teams VALUES (1, "3140", 1, 1);
    INSERT INTO scout.teams VALUES (2, "1234", 1, 2);

    SELECT teams.teamnumber, questions.question, choices.choice 
    FROM teams 
    INNER JOIN questions 
        ON teams.question = questions.id
    INNER JOIN choices 
        ON teams.choice = choices.id;
