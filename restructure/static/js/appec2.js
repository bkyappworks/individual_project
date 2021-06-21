console.log('https://bkyproductjobhuntingdashboard.com/')
const hov  = document.querySelector(".hov") 
const jobList = document.querySelector(".joblist") //jobList
//try
const jobList1 = document.querySelector(".joblist1")
const comList1 = document.querySelector(".com")
const urlList1 = document.querySelector(".url")
const btnList1 = document.querySelector(".btn1")
let nano = document.querySelector(".load-5");
nano.style.display = 'none';
// let nano1 = document.querySelector(".load-51");
// nano1.style.display = 'none';

//rec
const recList = document.querySelector(".reclist") //<section class="reclist">

const jobChoose = document.querySelector('select'); //jobChoose
//rec
// const jobRec = document.querySelector('.get-rec');
// const jobDisplay = document.querySelector('pre');

//default
var ctxR = document.getElementById("radarChart").getContext('2d');
var myRadarChart = new Chart(ctxR, {
    type: 'radar',
    data: {
    labels: ['SQL','Python','ETL','Javascript','Spark'],
    datasets: [
        {
            label: "Default, click Skills Need to see real skillsets",
            data: [1,1,1,0,0], //65, 59, 90, 81, 56, 55, 40
            backgroundColor: [
            'rgba(61, 90, 128, .5)',
            ],
            borderColor: [
            'rgba(61, 90, 128, 1)',
            ],
            borderWidth: 2
        }
    ]
    },
    options: 
    {
        responsive: true
    }
});

jobChoose.onchange = function() {
    const job = jobChoose.value;
    updateDisplay(job);
};

function updateDisplay(job) {
    let url = 'https://bkyproductjobhuntingdashboard.com/jobinfo'+'?type='+job; 
    let request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'text';
    request.onload = function() {
        let data = request.response;
        // jobDisplay.textContent = data;
        // console.log(data)

        //1. to json
        let dataparse = JSON.parse(data); 
        // let info = data['jobinfo']
        // console.log(info) //47
        // console.log(info[0]["company"]) //Facebook
        let jobsArray = dataparse['jobinfo']
        // let recArray = dataparse['recommend']
        // console.log(recArray)
        
        //2. loop through item
        jobList.innerHTML = '';
        //try
        jobList1.innerHTML = '';
        comList1.innerHTML = '';
        urlList1.innerHTML = '';
        btnList1.innerHTML = '';

        //line chart

        let trendArray = dataparse['trend']
        var ctxL = document.getElementById("lineChart").getContext('2d');
        var myLineChart = new Chart(ctxL, {
        type: 'line',
        data: {
            labels: JSON.parse(trendArray[0])["time"], //["January", "February", "March", "April", "May", "June", "July"]
            datasets: [
                {
                    label: "Data Engineer",
                    data: JSON.parse(trendArray[0])["de"], //[65, 59, 80, 81, 56, 55, 40]
                    backgroundColor: [
                        'rgba(24, 78, 119, .2)',
                        ],
                        borderColor: [
                        'rgba(24, 78, 119, .7)',
                    ],
                    borderWidth: 2
                },
                {
                    label: "Data Scientist",
                    data: JSON.parse(trendArray[0])["ds"], 
                    backgroundColor: [
                        'rgba(22, 138, 173, .2)',
                        ],
                    borderColor: [
                    'rgba(22, 138, 173, .7)',
                    ],
                    borderWidth: 2
                },
                {
                    label: "Data Analyst",
                    data: JSON.parse(trendArray[0])["da"], 
                    backgroundColor: [
                        'rgba(52, 160, 164, .2)',
                        ],
                        borderColor: [
                        'rgba(52, 160, 164, .7)',
                        ]
                    ,
                    borderWidth: 2
                },
                {
                    label: "Software Engineer",
                    data: JSON.parse(trendArray[0])["se"], 
                    backgroundColor: [
                        'rgba(82, 182, 154, .2)',
                        ],
                        borderColor: [
                        'rgba(82, 182, 154, .7)',
                        ]
                    ,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true
        }
        });
        
        for (let [key, value] of Object.entries(jobsArray)) {
            // console.log("key: ",key,"value: ", value);
            // console.log(jobsArray[key]);
            let jobs = document.createElement("h1");
            let node_position = document.createElement("h3");
            let node_company = document.createElement("h3");
            let node_url = document.createElement("h3");
            //try 
            let node_position_tr = document.createElement("tr");
            let node_aparts = document.createElement("div");
            let node_apart = document.createElement("div");
            node_aparts.className = "border-top my-3"
            let node_company_tr = document.createElement("tr");
            let node_url_tr = document.createElement("a");
            node_url_tr.href = jobsArray[key]['url']

            let node_tr = document.createElement("tr");
            // let node_btn = document.createElement("button").style.border = "thick solid #0000FF";
            let node_btn = document.createElement("button");
            let node_btn1 = document.createElement("button");

            node_btn.className = key;

            node_btn.className = "mr-2"
            node_btn.className = "btn btn-primary";
    
            node_btn1.className = "mr-2"
            node_btn1.className = "btn btn-light"; //btn-light

            node_btn.setAttribute("type", "button");
            node_btn1.setAttribute("type", "button");

            //click rec button
            node_btn.addEventListener('click', function() {
                // nano1.style.display = 'none';
                nano.style.display = 'inline';
                const jobid = jobsArray[key]['job_id'];
                // const jobid = node_btn.value
                let url1 = 'https://bkyproductjobhuntingdashboard.com/jobinfo?type='+job+'&choosejob='+jobid
                // console.log('url1: '+url1)
                // console.log ('job_id: '+jobid);
                let request1 = new XMLHttpRequest();
                // loading
    
                // let nano = document.querySelector(".nano");
                // nano.src = './static/vendor/Spinner.gif';
                
                // nano.style.display = 'inline';
                // recList1.innerHTML = '';
            
                request1.open('GET', url1);
                request1.responseType = 'text';
                request1.onload = function() {
                    
                    let data1 = request1.response;
                    // console.log(data1)
                    let dataparse1 = JSON.parse(data1); 
                    // console.log(dataparse1)
                    let recArray = dataparse1['recommend']
                    // recList1.innerHTML = '';
                    // document.querySelector(".loading").remove('nano')
                    nano.style.display = 'none';
                    
                    // recList1.innerHTML = '';
                    const recList1 = document.querySelector(".rec1")  
                    recList1.innerHTML = '';

                    for (let [key, value] of Object.entries(recArray)) {
                        // console.log('done')
                        let node_position_rec = document.createElement("div");
                        let node_url_rec = document.createElement("a");
                        node_url_rec.href = recArray[key]['url']
                        let node_apart = document.createElement("div");
                        // node_apart.innerHTML = '';
                        node_apart.className = "border-top my-3"
                        node_position_rec.innerText = recArray[key]["position"]+', '+recArray[key]['company']
                        // node_url_rec.innerText = recArray[key]['url']
                        node_url_rec.innerText = " => Click to see Full JD"
                        recList1.appendChild(node_apart)
                        node_apart.appendChild(node_position_rec)
                        node_apart.appendChild(node_url_rec)

                    };
                };
                request1.send();
            });

            //click radarChart
            node_btn1.addEventListener('click', function() {                
                // myRadarChart.reset();
                // myRadarChart.destroy();
                // ctxR.innerHTML = '';
                // ctxR.style.display = 'none';
                // myRadarChart.style.display = 'none';
                // let nano1 = document.querySelector(".load-51");
                // nano1.style.display = 'inline';
                
                const jobid = jobsArray[key]['job_id'];
                let url2 = 'https://bkyproductjobhuntingdashboard.com/jobinfo?type='+job+'&choosejob='+jobid+'&score='+jobid
                let request2 = new XMLHttpRequest();
                request2.open('GET', url2);
                request2.responseType = 'text';

                request2.onload = function() {
                    let data2 = request2.response;
                    let dataparse2 = JSON.parse(data2); 
                    // console.log(dataparse2)
                    let scoreArray = dataparse2['score']
                    // nano1.style.display = 'none';
                    // nano1.remove()
                    var ctxR = document.getElementById("radarChart").getContext('2d');
                    console.log(ctxR)
                    var myRadarChart = new Chart(ctxR, {
                        type: 'radar',
                        data: {
                        labels: scoreArray['skills'],
                        datasets: [
                            {
                                label: "Top Skills for the Job",
                                data: scoreArray['scores'], //65, 59, 90, 81, 56, 55, 40
                                backgroundColor: [
                                'rgba(61, 90, 128, .5)',
                                ],
                                borderColor: [
                                'rgba(61, 90, 128, 1)',
                                ],
                                borderWidth: 2
                            }
                        ]
                        },
                        options: 
                        {
                            responsive: true
                        }
                    });
                    // ctxR.remove();
                    // myRadarChart.clear();
                
            
            };
                request2.send();

        });
    

            jobs.innerText = "Jobs as follows: "
   
            node_position.innerText = jobsArray[key]["position"]
            node_company.innerText = jobsArray[key]['company']
            node_url.innerText = jobsArray[key]['url']
 
            //try
            node_position_tr.innerText = jobsArray[key]["position"]+', '+jobsArray[key]['company']
            node_position_tr.style.fontWeight = 'bold';
            node_url_tr.innerText = " => Click to see Full JD"
            node_btn.innerText ='Similar Jobs'
            node_btn1.innerText ='Skills Needed'

            // node_url.setAttribute("src",jobsArray[key]['url'])

            // // jobList.appendChild(jobs)
            // jobList.appendChild(node_position)
            // jobList.appendChild(node_company)
            // jobList.appendChild(node_url)
            //try
            node_aparts.appendChild(node_position_tr)
            jobList1.appendChild(node_aparts)
            node_aparts.appendChild(node_company_tr)
            // comList1.appendChild(node_aparts)
            node_aparts.appendChild(node_url_tr)
            // urlList1.appendChild(node_aparts)
            
            // urlList1.appendChild(node_url_tr)
            node_aparts.appendChild(node_tr)
            node_tr.appendChild(node_btn1)
            // node_tr.appendChild(node_apart)
            node_tr.appendChild(node_btn)
            // btnList1.appendChild(node_tr)
            btnList1.appendChild(node_aparts)
            
        }
    };
request.send();
};
  
updateDisplay('Data Engineer');
jobChoose.value = 'Data Engineer';