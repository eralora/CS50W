document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox == "open_mail") {
    open_mail();
    return;
  }

  fetch (`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((element) => {
        if (mailbox != "sent") {
          sender_recipients = element.sender;
        } else {
          sender_recipients = element.recipients;
        }
        // If read == true : grey background
        if (mailbox == "inbox") {
          // read1 it is a key for changing colors
          if (element.read) is_read ="read1";
          
          else is_read = '';
        } else is_read = "";

        var item = document.createElement('div');
        // Box for each mails
        // ${is_read} how do you change colors???
        item.className = `card my-1 ${is_read} items`;
        item.innerHTML = `<div class="card-body" id="item-${element.id}">
        ${element.subject} | ${sender_recipients} | ${element.timestamp}
        <br>
        ${element.body.slice(0,100)}
        </div>`;
        document.querySelector("#emails-view").appendChild(item);
        item.addEventListener("click", () =>{
          open_mail(element.id, mailbox);
        })
      })
    })

}

function open_mail(id, mailbox) {
  fetch (`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      console.log(email);
    document.querySelector("#emails-view").innerHTML = "";
    var item = document.createElement("div");
    item.className = `card`;
    item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
  Sender: ${email.sender}
  Recipients: ${email.recipients}
  Subject: ${email.subject}
  Time: ${email.timestamp}
  <br>
  ${email.body}
  </div>`;
  // Showing all above in browser
  document.querySelector("#emails-view").appendChild(item);
  // Archiving mails
  if (mailbox == "sent") return;
  let archive = document.createElement("btn");
  archive.className = `btn btn-outline-info my-2`;
  archive.addEventListener("click", () => {
    archive_mail(id, email.archived);
    if (archive.innerHTML == "Archive") archive.innerHTML = "Unarchive";
    else archive.innerHTML = "Archive"
  });
  if (!email.archived) archive.textContent = "Archive";
  else archive.textContent = "Unarchive";

  document.querySelector("#emails-view").appendChild(archive);



  // Reply email
  let reply = document.createElement("btn");
  reply.className = `btn btn-outline-success m-2`;
  reply.textContent = "Reply";
  reply.addEventListener("click", () => {
    reply_email(email.sender, email.subject, email.body, email.timestamp);
  });
  document.querySelector("#emails-view").appendChild(reply);
  mail_read(id);

    })
}


function archive_mail(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    })
  })
  load_mailbox("inbox");
}

function mail_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    })
  })
}

function reply_email(sender, subject, body, timestamp) {
  compose_email();
  if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;
  pre_fill = `On ${timestamp} ${sender} wrote:\n${body}\n`;
  document.querySelector("#compose-body").value = pre_fill;
}