let currentIndex = 0;
let intervalId;
let teamMembers = [];

fetch('../data/team-members.json')
    .then(response => response.json())
    .then(data => {
        teamMembers = data;

        showMember(currentIndex);

        startSlideshow();
    })
    .catch(error => console.error('Error fetching team members:', error));

function showMember(index) {
    const member = teamMembers[index]

    document.getElementById('member-image').src = member.image;
    document.getElementById('member-image').alt = member.name;
    document.getElementById('member-name').textContent = member.name;
    document.getElementById('member-description').textContent = member.description;
}

function startSlideshow() {
    intervalId = setInterval(() => {
        currentIndex = (currentIndex + 1) % teamMembers.length;
        showMember(currentIndex);
    }, 3000);
}

function stopSlideshow() {
    clearInterval(intervalId);
}

const memberSection = document.getElementById('team-members');
memberSection.addEventListener('mouseenter', stopSlideshow);
memberSection.addEventListener('mouseleave', startSlideshow);