let main_container = document.getElementById('main-container');
        
        
        function fetchEvents(type) {
            main_container.style.display = '';
            fetch('/get_events?type=' + type)
                .then(response => response.json())
                .then(events => {
                    let eventsContainer = document.getElementById('events-container');
                    eventsContainer.innerHTML = ''; // Clear the container
                    for (let event of events) {
                        let image = event.image;
                        eventsContainer.innerHTML += `
                        <div class="col-md-4">
                            <div class="card bg-dark text-white">
                                <div class="card-body">
                                    <img src="static/img/${event.image}" class="card-img-top" alt="Dummy Photo">
                                    <h5 class="card-title">${event.title}</h5>
                                    <p class="card-text">${event.description}</p>
                                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#eventModal${event.id}">Learn More</button>
                                   
                                </div>
                            </div>
                        </div>
                        `;
                    }
                    eventsContainer.innerHTML += `
                    
                    <h2 style="margin-top:50px;">----------All Events----------</h2>
                    `
                    
                   
                });
                
        }
        
        

        function fetchLikes(imageId,action) {
        
            
            
            // Make a POST request to update the likes column
            fetch(`/update_likes/${imageId}/${action}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                console.log(data);
               
            })
            .catch(error => {
                console.error('Error:', error);
            });
            let likeButton = document.getElementById(`like/${imageId}`);
            let dislikeButton = document.getElementById(`dislike/${imageId}`);
            let likeCount = document.getElementById(`img/${imageId}`);
            if (action == 'like') {
                likeButton.disabled = true;
                dislikeButton.disabled = false;
                likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1;
            } else {
                dislikeButton.disabled = true;
                likeButton.disabled = false;
                likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1;
            }

            

        }

        function myEvents() {
            main_container.style.display = 'none';
            fetch('/get_my_events')
                .then(response => response.json())
                .then(events => {
                    let eventsContainer = document.getElementById('events-container');
                    eventsContainer.innerHTML = ''; // Clear the container
                    for (let event of events) {
                        let image = event.image;
                        eventsContainer.innerHTML += `
                        <div class="col-md-4">
                            <div class="card bg-dark text-white">
                                <div class="card-body">
                                    <img src="static/img/${event.image}" class="card-img-top" alt="Dummy Photo">
                                    <h5 class="card-title">${event.title}</h5>
                                    <p class="card-text">${event.description}</p>
                                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editEventModal${event.id}">Edit</button>
                                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#deleteEventModal${event.id}">Delete</button>
                                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#eventModal${event.id}">Manage</button>
                                 </div>
                            </div>
                        </div>
                        `;
                    }
                })}

                jQuery("document").ready(function($){ var flakes = '', randomColor; for(var i = 0, len = 400; i < len; i++) { randomColor = Math.floor(Math.random()*16777215).toString(16); flakes += '<div class="ball" style="background: #'+randomColor; flakes += '; animation-duration: '+(Math.random() * 9 + 2)+'s; animation-delay: '; flakes += (Math.random() * 2 + 0)+'s;"></div>'; } document.getElementById('confetti').innerHTML = flakes;});
