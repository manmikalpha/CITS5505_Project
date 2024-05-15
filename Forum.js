document.addEventListener('DOMContentLoaded', function() {
    const submitQuestionBtn = document.getElementById('submitQuestion');
    const newQuestionInput = document.getElementById('newQuestion');
    const questionsArea = document.getElementById('questionsArea');

    submitQuestionBtn.addEventListener('click', function() {
        const questionText = newQuestionInput.value.trim();
        if (questionText) {
            addQuestion(questionText);
            newQuestionInput.value = ''; // Clear input field after adding question
        }
    });

    function addQuestion(questionText) {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item my-3 p-3 shadow-sm rounded';
        questionItem.innerHTML = `<span class="question-text"><strong>Question:</strong> ${questionText}</span>
            <button class="btn btn-primary btn-sm answer-btn">Answer</button>
            <div class="answer-list mt-3"></div>`;
        
        const answerBtn = questionItem.querySelector('.answer-btn');
        answerBtn.addEventListener('click', function() {
            if (!this.nextElementSibling.querySelector('form')) { // Prevent multiple forms
                const answerForm = document.createElement('form');
                answerForm.className = 'answer-form mt-2';
                answerForm.innerHTML = `<div class="input-group">
                    <input type="text" class="form-control" placeholder="Your answer...">
                    <button class="btn btn-outline-secondary" type="submit">Submit</button>
                    <button class="btn btn-outline-danger" type="button">X</button>
                </div>`;
                answerForm.addEventListener('submit', function(event) {
                    event.preventDefault();
                    const answerInput = this.querySelector('input');
                    const answerText = answerInput.value.trim();
                    if (answerText) {
                        let answerList = questionItem.querySelector('.answer-list');
                        if (!answerList.querySelector('.answer-title')) {
                            const answerTitle = document.createElement('div');
                            answerTitle.className = 'answer-title';
                            answerTitle.innerHTML = `<strong>Answer:</strong>`;
                            answerList.appendChild(answerTitle);
                        }
                        const answerItem = document.createElement('div');
                        answerItem.className = 'answer-item p-2';
                        answerItem.textContent = answerText;
                        answerList.appendChild(answerItem);
                        answerForm.remove(); // Remove form after submitting answer
                    }
                });

                // Add functionality to remove form
                answerForm.querySelector('.btn-outline-danger').addEventListener('click', function() {
                    answerForm.remove();
                });

                answerBtn.nextElementSibling.appendChild(answerForm);
            }
        });

        questionsArea.appendChild(questionItem);
    }
});
