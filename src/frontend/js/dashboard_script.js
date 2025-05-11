document.addEventListener("DOMContentLoaded", function () {

   document.getElementById("initial-loader").style.display = "block";

   fetchPendingQueries();

   setupTabs();

   document
     .getElementById("close-modal")
     .addEventListener("click", closeModal);
   window.addEventListener("click", function (event) {
     if (event.target === document.getElementById("query-modal")) {
       closeModal();
     }
   });

   document
     .getElementById("response-form")
     .addEventListener("submit", function (event) {
       event.preventDefault();
       submitResponse();
     });
 });

 function setupTabs() {
   const tabs = document.querySelectorAll('.tab');
   tabs.forEach(tab => {
     tab.addEventListener('click', function() {

       document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
       document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

       this.classList.add('active');


       const tabName = this.getAttribute('data-tab');
       document.getElementById(`${tabName}-section`).classList.add('active');

       if (tabName === 'unresolved' && document.getElementById('unresolved-queries').children.length <= 1) {
         document.getElementById("unresolved-loader").style.display = "block";
         fetchUnresolvedQueries();
       } else if (tabName === 'resolved' && document.getElementById('resolved-queries').children.length <= 1) {
         document.getElementById("resolved-loader").style.display = "block";
         fetchResolvedQueries();
       }
     });
   });
 }

 async function fetchPendingQueries() {
   try {
     const response = await fetch(
       "http://127.0.0.1:8000/api/query-request/pending-query"
     );

     if (!response.ok) {
       throw new Error("Failed to fetch queries");
     }

     const queries = await response.json();
     document.getElementById("initial-loader").style.display = "none";
     displayQueries(queries);
   } catch (error) {
     console.error("Error:", error);
     document.getElementById("initial-loader").style.display = "none";
     document.getElementById("pending-queries").innerHTML = `
               <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
                   <h3>Error fetching queries</h3>
                   <p>Please check if the API server is running.</p>
               </div>
           `;
   }
 }

 async function fetchUnresolvedQueries() {
   try {
     const response = await fetch(
       "http://127.0.0.1:8000/api/query-request/get-unresolved-queries"
     );

     if (!response.ok) {
       throw new Error("Failed to fetch unresolved queries");
     }

     const unresolvedQueries = await response.json();
     document.getElementById("unresolved-loader").style.display = "none";
     displayUnresolvedQueries(unresolvedQueries);
   } catch (error) {
     console.error("Error:", error);
     document.getElementById("unresolved-loader").style.display = "none";
     document.getElementById("unresolved-queries").innerHTML = `
       <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
         <h3>Error fetching unresolved queries</h3>
         <p>Please check if the API server is running.</p>
       </div>
     `;
   }
 }

 async function fetchResolvedQueries() {
   try {
     const response = await fetch(
       "http://127.0.0.1:8000/api/knowledge-base/resolved-queries"
     );

     if (!response.ok) {
       throw new Error("Failed to fetch resolved queries");
     }

     const resolvedQueries = await response.json();
     document.getElementById("resolved-loader").style.display = "none";
     displayResolvedQueries(resolvedQueries);
   } catch (error) {
     console.error("Error:", error);
     document.getElementById("resolved-loader").style.display = "none";
     document.getElementById("resolved-queries").innerHTML = `
       <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
         <h3>Error fetching resolved queries</h3>
         <p>Please check if the API server is running.</p>
       </div>
     `;
   }
 }

 function displayQueries(queries) {
   const container = document.getElementById("pending-queries");

   if (queries.length === 0) {
     container.innerHTML = `
               <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
                   <h3>No pending queries</h3>
                   <p>All customer queries have been addressed.</p>
               </div>
           `;
     return;
   }

   container.innerHTML = "";

   queries.forEach((query) => {
     const date = new Date(query.created_at);
     const formattedDate = date.toLocaleString();

     const card = document.createElement("div");
     card.className = "card";
     card.innerHTML = `
               <div class="status-badge"><span class="math-inline">\{query\.status\}</div\>
               <h3\>Query \#</span>{query.id}</h3>
               <p>${
                 query.question.length > 150
                   ? query.question.substring(0,150) + "...": query.question
               }</p>
               <div class="date">Received: ${formattedDate}</div>
           `;

     card.addEventListener("click", function () {
       openModal(query);
     });

     container.appendChild(card);
   });
 }

 function displayUnresolvedQueries(queries) {
   const container = document.getElementById("unresolved-queries");

   if (queries.length === 0) {
     container.innerHTML = `
       <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
         <h3>No unresolved queries</h3>
         <p>There are no unresolved customer queries.</p>
       </div>
     `;
     return;
   }

   container.innerHTML = "";

   queries.forEach((query) => {
     const date = new Date(query.created_at);
     const formattedDate = date.toLocaleString();

     const card = document.createElement("div");
     card.className = "card";
     card.innerHTML = `
       <div class="unresolved-badge">UNRESOLVED</div>
       <h3>Query #${query.id}</h3>
       <p>${
         query.question.length > 150
           ? query.question.substring(0, 150) + "..."
           : query.question
       }</p>
       <div class="date">Received: ${formattedDate}</div>
     `;

     card.addEventListener("click", function () {
       openModal(query);
     });

     container.appendChild(card);
   });
 }

 function displayResolvedQueries(queries) {
   const container = document.getElementById("resolved-queries");

   if (queries.length === 0) {
     container.innerHTML = `
       <div style="text-align: center; grid-column: 1 / -1; padding: 30px;">
         <h3>No resolved queries</h3>
         <p>There are no resolved customer queries in the system.</p>
       </div>
     `;
     return;
   }

   container.innerHTML = "";

   queries.forEach((query) => {
     const date = new Date(query.resolved_at);
     const formattedDate = date.toLocaleString();

     const card = document.createElement("div");
     card.className = "card";
     card.innerHTML = `
       <div class="resolved-badge">RESOLVED</div>
       <h3>Query #${query.id}</h3>
       <p>${
         query.question.length > 150
           ? query.question.substring(0, 150) + "..."
           : query.question
       }</p>
       <p><strong>Answer:</strong> ${
         query.answer.length > 100
           ? query.answer.substring(0, 100) + "..."
           : query.answer
       }</p>
       <div class="date">Resolved: ${formattedDate}</div>
     `;

     card.addEventListener("click", function() {
       showResolvedQueryDetails(query);
     });

     container.appendChild(card);
   });
 }

 function openModal(query) {
   const modal = document.getElementById("query-modal");
   const questionElement = document.getElementById("modal-question");
   const dateElement = document.getElementById("modal-date");
   const queryIdInput = document.getElementById("query-id");
   const answerElement = document.getElementById("answer");
   const submitButton = document.getElementById("submit-btn");

   questionElement.textContent = query.question;
   dateElement.textContent = `Received: ${new Date(
     query.created_at
   ).toLocaleString()}`;
   queryIdInput.value = query.id;

   answerElement.value = "";
   answerElement.readOnly = false;
   submitButton.style.display = "block";

   modal.style.display = "flex";

   document.getElementById("status-message").style.display = "none";
   document.getElementById("submit-btn").disabled = false;
 }

 function showResolvedQueryDetails(query) {
   const modal = document.getElementById("query-modal");
   const questionElement = document.getElementById("modal-question");
   const dateElement = document.getElementById("modal-date");
   const queryIdInput = document.getElementById("query-id");
   const answerElement = document.getElementById("answer");
   const submitButton = document.getElementById("submit-btn");

   questionElement.textContent = query.question;
   dateElement.textContent = `Resolved: ${new Date(query.resolved_at).toLocaleString()}`;
   queryIdInput.value = query.id;

   answerElement.value = query.answer;
   answerElement.readOnly = true;

   submitButton.style.display = "none";

   modal.style.display = "flex";
   document.getElementById("status-message").style.display = "none";
 }

 function closeModal() {
   document.getElementById("query-modal").style.display = "none";
 }

 async function submitResponse() {
   const queryId = document.getElementById("query-id").value;
   const answer = document.getElementById("answer").value.trim();
   const question = document.getElementById("modal-question").textContent;

   if (!answer) {
     return;
   }

   const submitBtn = document.getElementById("submit-btn");
   const loader = document.getElementById("submit-loader");
   const statusMessage = document.getElementById("status-message");

   submitBtn.disabled = true;
   loader.style.display = "block";
   statusMessage.style.display = "none";

   try {

     const resolveResponse = await fetch(
       "http://127.0.0.1:8000/api/query-request/resolve-query/",
       {
         method: "POST",
         headers: {
           "Content-Type": "application/json",
         },
         body: JSON.stringify({
           query_id: queryId,
         }),
       }
     );

     if (!resolveResponse.ok) {
       const errorData = await resolveResponse.json();
       throw new Error(
         errorData.message || "Failed to mark query as resolved"
       );
     }

     const addKnowledgeResponse = await fetch(
       "http://127.0.0.1:8000/api/knowledge-base/add-knowledge/",
       {
         method: "POST",
         headers: {
           "Content-Type": "application/json",
         },
         body: JSON.stringify({
           question: question,
           answer: answer,
           source: "SUPERVISOR",
           knowledge_type: "QUERY",
           description: {},
           description_key: "",
           query_request_id: queryId,
         }),
       }
     );

     loader.style.display = "none";

     if (addKnowledgeResponse.ok) {
       statusMessage.className = "status-message success";
       statusMessage.textContent =
         "Query resolved and response submitted successfully";

       setTimeout(() => {
         window.location.reload();
       }, 1000);
     } else {
       const errorData = await addKnowledgeResponse.json();
       throw new Error(errorData.message || "Failed to submit response");
     }
   } catch (error) {
     console.error("Error:", error);
     statusMessage.className = "status-message error";
     statusMessage.textContent =
       error.message || "Failed to submit response";
     submitBtn.disabled = false;
     loader.style.display = "none";
   }

   statusMessage.style.display = "block";
 }