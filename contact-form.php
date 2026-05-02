<?php
// Include PHPMailer classes from Composer
require 'vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Sanitize and collect input data
$name = strip_tags(trim($_POST['fname'] ?? ''));
$lastName = strip_tags(trim($_POST['lname'] ?? ''));
$emailHelp = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$phone = strip_tags(trim($_POST['phone'] ?? ''));
$comments = strip_tags(trim($_POST['message'] ?? ''));

// Basic validation
if (!empty($name) && !empty($phone) && filter_var($emailHelp, FILTER_VALIDATE_EMAIL)) {

	$mail = new PHPMailer(true);

	try {
		// --- Real Production Settings ---
		$mail->isSMTP();
		$mail->Host       = 'mail.thecaring.co.uk';
		$mail->SMTPAuth   = true;
		$mail->Username   = 'info@thecaring.co.uk';
		$mail->Password   = 'CLIENTS_REAL_PASSWORD'; // Client must enter their password here
		$mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS; // Use SSL
		$mail->Port       = 465;

		// --- Recipients ---
		$mail->setFrom('noreply@thecaring.co.uk', $name);
		$mail->addAddress('info@thecaring.co.uk', 'Admin');
		$mail->addReplyTo($emailHelp, $name);

		// --- Content ---
		$mail->isHTML(true);
		$mail->Subject = "New Inquiry from " . $name . " " . $lastName;

		$message_body = "Dear Admin,<br><br>";
		$message_body .= "The user whose detail is shown below has sent this message from " . htmlspecialchars($_SERVER['HTTP_HOST']) . ".<br><br>";
		$message_body .= "<b>Name:</b> " . htmlspecialchars($name . " " . $lastName) . "<br>";
		$message_body .= "<b>Email Address:</b> " . htmlspecialchars($emailHelp) . "<br>";
		$message_body .= "<b>Phone:</b> " . htmlspecialchars($phone) . "<br><br>";
		$message_body .= "<b>Message:</b><br>" . nl2br(htmlspecialchars($comments)) . "<br><br>";
		$message_body .= "Thank You!";

		$mail->Body = $message_body;

		$mail->send();
		$status = 'Success';
		$output = "Congrats " . htmlspecialchars($name) . ", your message has been sent to our testing inbox!";

	} catch (Exception $e) {
		$status = 'error';
		$output = "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
	}

} else {
	$status = 'error';
	$output = "Please fill in all required fields correctly (Valid Name, Email, and Phone).";
}

echo json_encode(array('status' => $status, 'msg' => $output));
?>