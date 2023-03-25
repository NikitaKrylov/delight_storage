new Chart(document.getElementById('dashboard1'), {
    type: 'bar',
    data: {
        labels: tlabelsList,
        datasets: [{
            label: 'Постов',
            data: tvaluesList,
            borderWidth: 1,
        }],
    },

    options: {
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    },
});

new Chart(document.getElementById('dashboard2'), {
    type: 'line',
    data: {
        labels: views_labelsList,
        datasets: [{
            label: 'Количество просмотров за день',
            data: views_valuesList,
            borderWidth: 1,
        }],
    },
    
    options: {
        animations: {
            tension: {
                duration: 2000,
                easing: 'linear',
                from: 0.5,
                to: 0,
                loop: true
            }
        },
    }

});

new Chart(document.getElementById('dashboard3'), {
    type: 'line',
    data: {
        labels: likes_labelsList,
        datasets: [{
            label: 'Количество лайков за день',
            data: likes_valuesList,
            borderWidth: 1,
        }],
    },

    options: {
        animations: {
            tension: {
                duration: 2000,
                easing: 'linear',
                from: 0.5,
                to: 0,
                loop: true
            }
        },
    }
});

new Chart(document.getElementById('dashboard4'), {
    type: 'line',
    data: {
        labels: sub_labelsList,
        datasets: [{
            label: 'Количество подписок за день',
            data: sub_valuesList,
            borderWidth: 1,
        }],
    },

    options: {
        animations: {
            tension: {
                duration: 2000,
                easing: 'linear',
                from: 0.5,
                to: 0,
                loop: true
            }
        },
    }
});

// new Chart(document.getElementById('all-dashboard'), {
//     type: 'line',
//     data: {
//         labels: tlabelsList,
//         datasets: [
//             {
//                 label: 'Постов',
//                 data: tvaluesList,
//                 borderWidth: 1,
//             },
//             {
//                 label: 'Количество просмотров за день',
//                 data: views_valuesList,
//                 borderWidth: 1,
//             },
//             {
//                 label: 'Количество лайков за день',
//                 data: likes_valuesList,
//                 borderWidth: 1,
//             },
//             {
//                 label: 'Количество подписок за день',
//                 data: sub_valuesList,
//                 borderWidth: 1,
//             },
//         ],
//     },

//     options: {
//         animations: {
//             tension: {
//                 duration: 2000,
//                 easing: 'linear',
//                 from: 0.5,
//                 to: 0,
//                 loop: true
//             }
//         },
//     }
// });
