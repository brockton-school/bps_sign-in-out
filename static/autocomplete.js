function fetchSuggestions(userType, grade) {
    const input = document.getElementById('name-input').value;
    const list = document.getElementById('autocomplete-list');
    
    // Clear any existing suggestions
    list.innerHTML = '';

    if (input.length < 2) {
        return;  // Start suggesting only when input has more than 2 characters
    }

    // Fetch suggestions from the server
    fetch(`/autocomplete?query=${input}&user_type=${userType}&grade=${grade}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const suggestionItem = document.createElement('div');
                suggestionItem.innerHTML = item;
                suggestionItem.classList.add('autocomplete-item');

                // When clicking on a suggestion, fill the input
                suggestionItem.addEventListener('click', function () {
                    document.getElementById('name-input').value = item;
                    list.innerHTML = '';  // Clear suggestions after selecting
                });

                list.appendChild(suggestionItem);
            });
        });
}