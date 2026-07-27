MEETING_CREATION_NOTIFICATION_SUBJECT = "New Collective Body Meeting / Νέα Συνεδρίαση Συλλογικού Οργάνου"

MEETING_CREATION_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              New Meeting Scheduled
            </h2>

            <p>Dear member,</p>

            <p>
              A new meeting has been scheduled for the collective body <strong>{collective_body_title_en}</strong>, 
              in which you participate. Your attendance is kindly requested.
            </p>

            <p>
              <strong>Meeting number:</strong> {index}<br>
              <strong>Date and Time:</strong> {date_and_time}<br>
              <strong>Location:</strong> {location}<br>
              <strong>Notes:</strong> {notes}
            </p>
            
            <p>
              If you are unable to attend, please inform the responsible secretariat accordingly at:
              <strong>{secretariat_email}</strong>
            </p>

          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td>
            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;">
          </td>
        </tr>

        <!-- Greek Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              Προγραμματίστηκε Νέα Συνεδρίαση
            </h2>

            <p>Αγαπητό μέλος,</p>

            <p>
              Έχει προγραμματιστεί νέα συνεδρίαση για το συλλογικό όργανο <strong>{collective_body_title_gr}</strong>,
              στο οποίο συμμετέχετε. Παρακαλείστε να παρευρεθείτε.
            </p>

            <p>
              <strong>Αριθμός Συνεδρίασης:</strong> {index}<br>
              <strong>Ημερομηνία και Ώρα:</strong> {date_and_time}<br>
              <strong>Τοποθεσία:</strong> {location}<br>
              <strong>Σημειώσεις:</strong> {notes}
            </p>

            <p>

            </p>

            <p>
              Σε περίπτωση που δεν μπορείτε να παρευρεθείτε, παρακαλούμε ενημερώστε σχετικά την αρμόδια γραμματεία στο:
              <strong>{secretariat_email}</strong>
            </p>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

MEETING_UPDATE_NOTIFICATION_SUBJECT = "Update of Meeting Details / Ενημέρωση Στοιχείων Συνεδρίασης"

MEETING_UPDATE_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              Meeting Details Updated
            </h2>

            <p>Dear member,</p>

            <p>
              The details of a scheduled meeting for the collective body <strong>{collective_body_title_en}</strong>,
              in which you participate have been updated.
            </p>

            <p>
              <strong>Date and Time:</strong> {date_and_time}<br>
              <strong>Location:</strong> {location}<br>
              <strong>Notes:</strong> {notes}
            </p>

            <p>
              If you are unable to attend, please inform the responsible secretariat accordingly at:
              <strong>{secretariat_email}</strong>
            </p>

          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td>
            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;">
          </td>
        </tr>

        <!-- Greek Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              Ενημέρωση Στοιχείων Συνεδρίασης
            </h2>

            <p>Αγαπητό μέλος,</p>

            <p>
              Τα στοιχεία προγραμματισμένης συνεδρίασης για το συλλογικό όργανο <strong>{collective_body_title_gr}</strong>,
              στο οποίο συμμετέχετε έχουν ενημερωθεί.
            </p>

            <p>
              <strong>Ημερομηνία και Ώρα:</strong> {date_and_time}<br>
              <strong>Τοποθεσία:</strong> {location}<br>
              <strong>Σημειώσεις:</strong> {notes}
            </p>

            <p>
              Σε περίπτωση που δεν μπορείτε να παρευρεθείτε, παρακαλούμε ενημερώστε σχετικά την αρμόδια γραμματεία στο:
              <strong>{secretariat_email}</strong>
            </p>
            
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

MEETING_CHANGED_BODY_OLD_MEMBERS_SUBJECT = "Meeting Reassignment / Αλλαγή Ανάθεσης Συνεδρίασης"

MEETING_CHANGED_BODY_OLD_MEMBERS_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">Meeting No Longer Concerns Your Collective Body</h2>

            <p>Dear member,</p>

            <p>
              The following meeting is no longer assigned to the collective body in which you participate.
              Therefore, you are no longer required to attend this meeting.
            </p>

            <p>
              <strong>Previous Collective Body:</strong> {old_collective_body_title_en}<br>
              <strong>Meeting Number:</strong> {index}<br>
              <strong>Date and Time:</strong> {date_and_time}<br>
              <strong>Location:</strong> {location}
            </p>

            <p>
              If you have any questions, please contact the responsible secretariat at:
              <strong>{old_secretariat_email}</strong>
            </p>
          </td>
        </tr>

        <tr>
          <td>
            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;">
          </td>
        </tr>

        <!-- Greek Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">Η Συνεδρίαση δεν αφορά πλέον το Συλλογικό σας Όργανο</h2>

            <p>Αγαπητό μέλος,</p>

            <p>
              Η παρακάτω συνεδρίαση δεν αφορά πλέον το συλλογικό όργανο στο οποίο συμμετέχετε.
              Επομένως, δεν απαιτείται πλέον η παρουσία σας στη συγκεκριμένη συνεδρίαση.
            </p>

            <p>
              <strong>Προηγούμενο Συλλογικό Όργανο:</strong> {old_collective_body_title_gr}<br>
              <strong>Αριθμός Συνεδρίασης:</strong> {index}<br>
              <strong>Ημερομηνία και Ώρα:</strong> {date_and_time}<br>
              <strong>Τοποθεσία:</strong> {location}
            </p>

            <p>
              Για οποιαδήποτε διευκρίνιση, μπορείτε να επικοινωνήσετε με την αρμόδια γραμματεία στο:
              <strong>{old_secretariat_email}</strong>
            </p>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
"""

MEETING_CHANGED_BODY_NEW_MEMBERS_SUBJECT = "Meeting Assignment / Ανάθεση Συνεδρίασης"
