
const selectBoxes = document.querySelectorAll('.select-box');
selectBoxes.forEach(selectBox => {
    const selectOption = selectBox.querySelector('.select-option');
    const inputField = selectBox.querySelector('input[readonly]');
    const optionSearch = selectBox.querySelector('#optionSearch');
    const optionsList = selectBox.querySelectorAll('.options li');
    selectOption.addEventListener('click',function(){
        selectBox.classList.toggle('active');
    });
    optionsList.forEach(function(optionsListSingle){
        optionsListSingle.addEventListener('click',function(){
            text = this.textContent;
            inputField.value = text;
            selectBox.classList.remove('active');
        })
    });
    optionSearch.addEventListener('keyup',function(){
        var filter, li, i, textValue;
        filter = optionSearch.value.toLowerCase();
        li = optionsList;
        for(i=0;i<li.length;i++){
            liCount = li[i];
            textValue = liCount.textContent || liCount.innerText;
            if (textValue.toLowerCase().indexOf(filter) > -1){
                li[i].style.display = '';
            }else{
                li[i].style.display = 'none';
            }
        }
    })
})
const stageInput = document.querySelector('#stageInput');
const timeInput = document.querySelector('#timeInput');
const timeLabel = document.querySelector('#timeLabel');
const optionsList = document.querySelectorAll('.options li');

optionsList.forEach(function(option){
    option.addEventListener('click', function() {
        const text = this.textContent;
        stageInput.value = text;
        toggleTimeInput(text);
        // Close dropdown after selection
        document.querySelector('.select-box').classList.remove('active');
    });
});

function toggleTimeInput(selectedStage) {
    // Adjust which stages require a time input
    const stagesThatRequireTimeInput = ['Job Opening','Phone/Video Screening Interview', 'Online Assessment', 'Interview', 'Job Offer'];
    if (stagesThatRequireTimeInput.includes(selectedStage)) {
        timeInput.style.display = 'block'; // Show the time input
        timeLabel.style.display = 'block'; //show the label for time input
        timeInput.required = true; // Set as required
    } else {
        timeInput.style.display = 'none'; // Hide the time input
        timeLabel.style.display = 'none';
        timeInput.required = false;
        timeInput.value = ''; // Clear the input value
    }
}
