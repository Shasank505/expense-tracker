// main.js — students will add JavaScript here as features are built

(function () {
    var modal = document.getElementById('videoModal');
    var openBtn = document.getElementById('openModal');
    var closeBtn = document.getElementById('closeModal');
    var iframe = document.getElementById('modalVideo');

    var youtubeUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    function openModal() {
        iframe.src = youtubeUrl;
        modal.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
        iframe.src = '';
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
})();
