document.addEventListener('DOMContentLoaded', function() {
    let recommendationLink = document.getElementById('recommendations-link');

    if (recommendationLink) {
        recommendationLink.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('Recommendation link clicked');
            showBlockContent();
        });
    }
});

function showBlockContent() {
    var profileCards = document.getElementById('profile-cards');
    var blockContent = document.getElementById('block-content');
    
    if (profileCards) {
        profileCards.style.display = 'none';
        console.log('Profile cards hidden');
    }
    if (blockContent) {
        blockContent.style.display = 'block';
        console.log('Block content displayed');
    }
}


