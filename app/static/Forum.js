$(document).ready(function() {
    $('#submitQuestion').click(function() {
        let questionText = $('#newQuestion').val().trim();
        if (questionText) {
            $.ajax({
                url: '/add_question',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({text: questionText}),
                success: function(data) {
                    let questionHTML = `<div class="question-item my-3 p-3 shadow-sm rounded" data-id="${data.id}">
                        <span class="question-text"><strong>Question:</strong> ${data.text}</span>
                        <button class="btn btn-primary btn-sm answer-btn">Answer</button>
                        <div class="answer-list mt-3"></div>
                    </div>`;
                    $('#questionsArea').append(questionHTML);
                    $('#newQuestion').val('');
                }
            });
        }
    });

    $(document).on('click', '.answer-btn', function() {
        let questionItem = $(this).closest('.question-item');
        if (!questionItem.find('form').length) {
            let answerFormHTML = `<form class="answer-form mt-2">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Your answer...">
                    <button class="btn btn-outline-secondary" type="submit">Submit</button>
                    <button class="btn btn-outline-danger" type="button">X</button>
                </div>
            </form>`;
            questionItem.append(answerFormHTML);
        }
    });

    $(document).on('click', '.answer-form .btn-outline-danger', function() {
        $(this).closest('form').remove();
    });

    $(document).on('submit', '.answer-form', function(event) {
        event.preventDefault();
        let answerText = $(this).find('input').val().trim();
        let questionItem = $(this).closest('.question-item');
        let questionId = questionItem.data('id');
        if (answerText) {
            $.ajax({
                url: '/add_answer',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({text: answerText, question_id: questionId}),
                success: function(data) {
                    let answerHTML = `<div class="answer-item p-2">${data.text}</div>`;
                    questionItem.find('.answer-list').append(answerHTML);
                    $(this).remove();
                }.bind(this)
            });
        }
    });
});
