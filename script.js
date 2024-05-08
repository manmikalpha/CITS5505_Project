document.addEventListener('DOMContentLoaded', function () {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(item => {
        const button = item.querySelector('.accordion-header .accordion-button');

        button.addEventListener('click', function () {
            const content = item.querySelector('.accordion-collapse');

            // If the content is collapsed, expand it; if it's expanded, collapse it
            if (content.classList.contains('collapse')) {
                content.classList.remove('collapse'); // Expand
            } else {
                content.classList.add('collapse'); // Collapse
            }

            // Collapse other accordion items except the current one
            accordionItems.forEach(otherItem => {
                if (otherItem !== item) {
                    const otherContent = otherItem.querySelector('.accordion-collapse');
                    otherContent.classList.add('collapse'); // Collapse
                }
            });
        });
    });
});
