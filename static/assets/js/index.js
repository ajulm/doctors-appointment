var url = "https://api.github.com/users/rustyyyyy/repos";

var xhr = new XMLHttpRequest();
xhr.open("GET", url);

xhr.setRequestHeader("Accept", "application/json");

xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
        // console.log(xhr.status);
        // console.log(xhr.responseText);
        var response = JSON.parse(xhr.responseText);
        
        let html = '';
        response.forEach(project => {
            let htmlSegment = `<tr>
                                    <td>${project.name} </td>
                                    <td><a style="color: #1900ff;" href="${project.html_url}">${project.html_url}</a></td>
                                    <td>${project.created_at} </td>
                                    <td>${project.language} </td>
                                </tr>
                            `;

            html += htmlSegment;
        });
         let container = document.getElementById('container');
        container.innerHTML = html;
   }};

xhr.send();