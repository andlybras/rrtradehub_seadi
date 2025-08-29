// core/static/core/js/reception.js

// Espera o documento HTML ser completamente carregado para executar o código
document.addEventListener('DOMContentLoaded', function() {
    // Encontra o container que guarda as imagens
    const slider = document.querySelector('.image-slider');
    // Pega todas as imagens de dentro do container
    const images = slider.querySelectorAll('img');

    // Só executa o código se houver imagens na página
    if (images.length > 0) {
        let currentIndex = 0; // Começa com a primeira imagem (índice 0)

        // Define um intervalo de tempo para executar a troca de imagens
        setInterval(() => {
            // 1. Remove a classe 'active' da imagem que está visível no momento
            images[currentIndex].classList.remove('active');

            // 2. Calcula qual será a próxima imagem a ser mostrada
            // O '%' faz com que o contador volte a 0 quando chegar ao fim da lista
            currentIndex = (currentIndex + 1) % images.length;

            // 3. Adiciona a classe 'active' na nova imagem, fazendo-a aparecer
            images[currentIndex].classList.add('active');

        }, 4000); // A troca acontece a cada 4 segundos (4000 milissegundos)
    }
});