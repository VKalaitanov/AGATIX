 document.addEventListener('DOMContentLoaded', () => {
  const customSelectElements = document.querySelectorAll('.custom-select');

  customSelectElements.forEach(customSelectElement => {
    const customSelectTrigger = customSelectElement.querySelector('.custom-select-trigger');
    const customOptions = customSelectElement.querySelector('.custom-options');
    const customOptionElements = customOptions.querySelectorAll('.custom-option');
    const hiddenInput = customSelectElement.querySelector('input[type="hidden"]');

    // Установка выбранного значения при загрузке страницы
    const selectedValue = hiddenInput.value;
    const selectedOption = customOptions.querySelector(`[data-value="${selectedValue}"]`);
    if (selectedOption) {
      customSelectElement.querySelector('.selected-option').textContent = selectedOption.textContent;
      selectedOption.classList.add('is-selected');
    }

    customSelectTrigger.addEventListener('click', () => {
      customOptions.classList.toggle('is-open');
      customSelectTrigger.classList.toggle('is-clicked');
      customSelectElement.classList.toggle('is-active');

    });

    customOptionElements.forEach(option => {
      option.addEventListener('click', () => {
        const selectedOption = option.getAttribute('data-value');
        const selectedText = option.textContent;

        const oldSelectedOption = customOptions.querySelector('.is-selected');
        if (oldSelectedOption) {
          oldSelectedOption.classList.remove('is-selected');
        }

        // Добавляем "is-selected" класс на новый выбранный элемент
        option.classList.add('is-selected');

        customSelectElement.querySelector('.selected-option').textContent = selectedText;
        hiddenInput.value = selectedOption;
        customOptions.classList.remove('is-open');
        customSelectElement.classList.toggle('is-active');
      });
    });
  });

  // Обработчик для всего документа
  document.addEventListener('click', (event) => {
    const isClickedElement = event.target.closest('.custom-select-trigger');

    customSelectElements.forEach(customSelectElement => {
      const customSelectTrigger = customSelectElement.querySelector('.custom-select-trigger');
      const customOptions = customSelectElement.querySelector('.custom-options');

      if (!isClickedElement || isClickedElement !== customSelectTrigger) {
        customSelectTrigger.classList.remove('is-clicked');
        customOptions.classList.remove('is-open');
        customSelectElement.classList.remove('is-active');
      }
    });
  });
});

