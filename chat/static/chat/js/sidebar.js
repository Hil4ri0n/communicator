function sideBar(choice){
    let optionsBar = document.querySelector('.options-bar');
    let emojiBar = document.querySelector('.emoji-bar');
    let emojiVisible = emojiBar.getAttribute('data-visible');
    let optionsVisible = optionsBar.getAttribute('data-visible');
    if(choice === 'options'){
        if(emojiVisible === 'true'){
            toggleBar(emojiBar);
        }
        toggleBar(optionsBar);
    }else{
       if(optionsVisible === 'true'){
           toggleBar(optionsBar);
       }
       toggleBar(emojiBar);
    }
}

function toggleBar(bar){
    let visible = bar.getAttribute('data-visible');
    if(visible === 'true'){
        bar.setAttribute('data-visible', 'false');
        bar.classList.add('hidden');
    } else{
        bar.setAttribute('data-visible', 'true');
        bar.classList.remove('hidden');
    }
}

function menuBar(element){
    let bar = element;
    let wrapper = bar.parentElement;
    let menu = wrapper.querySelector('.menu-list');
    let unwrapped = bar.getAttribute('data-unwrapped');
    let symbol = bar.getElementsByTagName('i')[0];
    if(unwrapped === 'false'){
        bar.setAttribute('data-unwrapped', 'true');
        menu.classList.remove('hidden');
        symbol.classList.replace('fa-greater-than', 'fa-v');
    }else{
        bar.setAttribute('data-unwrapped', 'false');
        menu.classList.add('hidden');
        symbol.classList.replace('fa-v','fa-greater-than');
    }
}