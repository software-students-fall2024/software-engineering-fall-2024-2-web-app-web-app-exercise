const locationSelectBox = document.querySelector('.select-box-location');
const stageSelectBox = document.querySelector('.select-box-stage');
function setupDropdown(selectBox){
    const selectOption = selectBox.querySelector('.select-option');
    const inputField = selectBox.querySelector('input[readonly]');
    const optionSearch = selectBox.querySelector('.search input');
    const optionsList = selectBox.querySelectorAll('.options li');
    selectOption.addEventListener('click',function(){
        selectBox.classList.toggle('active');
        console.log('Active class toggled:', selectBox.classList.contains('active'));
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
}
setupDropdown(locationSelectBox);
setupDropdown(stageSelectBox);