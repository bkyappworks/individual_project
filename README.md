# Quick Hunt - Your Job Hunting Dashboard
<h2>A Dashboard That: </h2>
<li> Automatically scrap and demonstrate new job postings from linkedin and Indeed </li>
<li> Show top skills for each job at a glance by extracting and analyzing data from (usually very long) job descriptions </li>
<li> Provide information not only about jobs but also the entire job searching trends based on Google Trend </li>

<h2>Website </h2>
https://bkyproductjobhuntingdashboard.com/ 

<h2>Technology</h2>

<h3>Backend</h3>
<li>Python
<li>Flask
<li>NGINX

<h3>Front-End</h3>
<li>HTML
<li>CSS
<li>JavaScript
<li>AJAX

<h3>Cloud Service (AWS)</h3>
<li>Compute: EC2
<li>Database: RDS

<h3>Automation</h3>
<li>Airflow

<h3>Tools</h3>
<li>Web Crawler: selenium, chromedriver, beautifulsoup
<li>Version Control: Git, GitHub
<li>Test: Unittest
<li>Agile: Trello (Scrum)

<h3>Database Design</h3>
<li>MySQL

<h2>Architecture</h2>
<li> Build flask as server and deploy server on AWS EC2
<li> Display information of API through AJAX 
<li> Implement Airflow to automate scraping once a week
<!-- Redirect port requests from clients by NGINX -->

![image](https://github.com/bkyappworks/individual_project/blob/master/images/Architeture.png)
<h2>Database</h2>

![image](https://github.com/bkyappworks/individual_project/blob/master/images/database_design.png)

<h2>Data Flow</h2>
<li> Scrap jobs from Linkedin and Indeed by selenium and beautifulsoup
<li> Integrate google trend API to demonstrate latest search trends
<li> Use ETL to clean and extract data from job description and save to AWS RDS

![image](https://github.com/bkyappworks/individual_project/blob/master/images/data_flow.png)

<h2>Contact</h2>

beckyappworks@gmail.com