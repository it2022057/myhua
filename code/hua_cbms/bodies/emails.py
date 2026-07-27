CREATION_NOTIFICATION_SUBJECT = "New Collective Body Creation / Δημιουργία Νέου Συλλογικού Οργάνου"

SEC_CREATION_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              New Collective Body Assigned 
            </h2>

            <p>Dear Secretariat,</p>

            <p>
              A new collective body has been created in the system and you have been assigned as responsible for its management.
            </p>

            <p>
              <strong>Title:</strong> {title_en}<br>
              <strong>Start Date:</strong> {start_date}<br>
              <strong>End Date:</strong> {end_date}
            </p>

            <p>
              You may <u>view</u> or <u>update</u> the collective body details, by logging in the platform.
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
              Ανατέθηκε νέο συλλογικό όργανο
            </h2>

            <p>Αξιότιμη Γραμματεία,</p>

            <p>
              Ένα νέο συλλογικό όργανο έχει δημιουργηθεί στο σύστημα και έχετε οριστεί υπεύθυνος για τη διαχείρισή του.
            </p>

            <p>
              <strong>Τίτλος:</strong> {title_gr}<br>
              <strong>Ημερομηνία Έναρξης:</strong> {start_date}<br>
              <strong>Ημερομηνία Λήξης:</strong> {end_date}
            </p>

            <p>
              Μπορείτε να <u>δείτε</u> ή να <u>ενημερώσετε</u> τα στοιχεία του συλλογικού οργάνου, πραγματοποιώντας είσοδο στην πλατφόρμα.
            </p>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

PRESIDENT_CREATION_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">Collective Body Presidency Assignment</h2>

            <p>Dear Sir/Madam {surname_en},</p>

            <p>
              A new collective body has been created in the system and you have been assigned as its president.
            </p>

            <p>
              <strong>Collective Body:</strong> {title_en}<br>
              <strong>Start Date:</strong> {start_date}<br>
              <strong>End Date:</strong> {end_date}
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
            <h2 style="margin-top:0; color:#1a73e8;">Ορισμός Προέδρου Συλλογικού Οργάνου</h2>

            <p>Αγαπητέ κύριε/Αγαπητή κυρία {surname_gr},</p>

            <p>
              Δημιουργήθηκε νέο συλλογικό όργανο στο σύστημα και έχετε οριστεί ως πρόεδρός του.
            </p>

            <p>
              <strong>Συλλογικό Όργανο:</strong> {title_gr}<br>
              <strong>Ημερομηνία Έναρξης:</strong> {start_date}<br>
              <strong>Ημερομηνία Λήξης:</strong> {end_date}
            </p>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

UPDATE_NOTIFICATION_SUBJECT = "Update of Collective Body / Ενημέρωση Συλλογικού Οργάνου"

UPDATE_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              Collective Body Updated
            </h2>

            <p>Dear President and members,</p>

            <p>
              The details of the following collective body have been updated in the system.
              The update may concern the title and/or the participant list of the collective body.
            </p>

            <p>
              <strong>Collective Body:</strong> {title_en}<br>
              <strong>Start Date:</strong> {start_date}<br>
              <strong>End Date:</strong> {end_date}
            </p>

            <p>
              <strong>Current members:</strong>
            </p>

            <table width="100%" cellpadding="6" cellspacing="0" style="border-collapse:collapse; margin:15px 0; font-size:14px;">
              <tr style="background-color:#f8f9fa;">
                <th align="left" style="border:1px solid #e0e0e0;">Full name</th>
                <th align="left" style="border:1px solid #e0e0e0;">Email</th>
              </tr>
              {participants_rows}
            </table>

            <p>
              Please check the updated information.
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
              Το συλλογικό όργανο ενημερώθηκε
            </h2>

            <p>Αγαπητέ/ή Πρόεδρε, αγαπητά μέλη,</p>

            <p>
              Τα στοιχεία του παρακάτω συλλογικού οργάνου ενημερώθηκαν στο σύστημα.
              Η ενημέρωση ενδέχεται να αφορά τον τίτλο ή/και τη σύνθεση των μελών του συλλογικού οργάνου.
            </p>

            <p>
              <strong>Συλλογικό Όργανο:</strong> {title_gr}<br>
              <strong>Ημερομηνία Έναρξης:</strong> {start_date}<br>
              <strong>Ημερομηνία Λήξης:</strong> {end_date}<br>
              <strong>Κατάσταση:</strong> {active}
            </p>

            <p>
              <strong>Τρέχοντα μέλη:</strong>
            </p>

            <table width="100%" cellpadding="6" cellspacing="0" style="border-collapse:collapse; margin:15px 0; font-size:14px;">
              <tr style="background-color:#f8f9fa;">
                <th align="left" style="border:1px solid #e0e0e0;">Ονοματεπώνυμο</th>
                <th align="left" style="border:1px solid #e0e0e0;">Email</th>
              </tr>
              {participants_rows}
            </table>

            <p>
              Παρακαλούμε ελέγξτε τα ενημερωμένα στοιχεία.
            </p>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

PARTICIPANT_ADDED_NOTIFICATION_SUBJECT = "Participation to Collective Body / Συμμετοχή σε Συλλογικό Όργανο"

PARTICIPANT_ADDED_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">
        
        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">Added to a Collective Body</h2>

            <p>Dear Sir or Madam,</p>

            <p>
              You have been added as a member to the following collective body:
            </p>

            <p>
              <strong>Title:</strong> {title_en}<br>
              <strong>President:</strong> {president_display_name_en}<br>
              <strong>Start Date:</strong> {start_date}<br>
              <strong>End Date:</strong> {end_date}
            </p>

            <p>
              You can now see the subjects, decisions and meetings concerning the new body, using the link below.
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:20px 0;">
              <tr>
                <td align="center" style="background:#1a73e8; padding:12px 22px; border-radius:4px;">
                  <a href="{url}" style="color:white; text-decoration:none; font-weight:bold;">
                    View Collective Body
                  </a>
                </td>
              </tr>
            </table>
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
            <h2 style="margin-top:0; color:#1a73e8;">Προσθήκη σε Συλλογικό Όργανο</h2>

            <p>Αγαπητέ/ή,</p>

            <p>
              Έχετε προστεθεί ως μέλος στο παρακάτω συλλογικό όργανο:
            </p>

            <p>
              <strong>Τίτλος:</strong> {title_gr}<br>
              <strong>Πρόεδρος:</strong> {president_display_name_gr}<br>
              <strong>Ημερομηνία Έναρξης:</strong> {start_date}<br>
              <strong>Ημερομηνία Λήξης:</strong> {end_date}
            </p>

            <p>
              Μπορείτε πλέον να δείτε τα θέματα, τις αποφάσεις και τις συνεδριάσεις που αφορούν το νέο όργανο, μέσω του παρακάτω συνδέσμου.
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:20px 0;">
              <tr>
                <td align="center" style="background:#1a73e8; padding:12px 22px; border-radius:4px;">
                  <a href="{url}" style="color:white; text-decoration:none; font-weight:bold;">
                    Προβολή Συλλογικού Οργάνου
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

PARTICIPANT_REMOVED_NOTIFICATION_SUBJECT = "Removal from Collective Body / Αφαίρεση από Συλλογικό Όργανο"

PARTICIPANT_REMOVED_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; padding:30px; border-radius:8px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">
              Removed from Collective Body
            </h2>

            <p>Dear Sir or Madam,</p>

            <p>
              You are no longer listed as a member of the following collective body:
            </p>

            <p>
              <strong>Title:</strong> {title_en}<br>
              <strong>President:</strong> {president_display_name_en}<br>
              <strong>Start Date:</strong> {start_date}<br>
              <strong>End Date:</strong> {end_date}
            </p>

            <p>
              For more information, please contact the responsible secretariat <u>{secretariat_email}</u>.
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
              Αφαιρεθήκατε από Συλλογικό Όργανο
            </h2>

            <p>Αγαπητέ/ή,</p>

            <p>
              Σας ενημερώνουμε ότι δεν συμμετέχετε πλέον ως μέλος στο παρακάτω συλλογικό όργανο:
            </p>

            <p>
              <strong>Τίτλος:</strong> {title_gr}<br>
              <strong>Πρόεδρος:</strong> {president_display_name_gr}<br>
              <strong>Ημερομηνία Έναρξης:</strong> {start_date}<br>
              <strong>Ημερομηνία Λήξης:</strong> {end_date}
            </p>

            <p>
              Για περισσότερες πληροφορίες, μπορείτε να επικοινωνήσετε με την αρμόδια γραμματεία <u>{secretariat_email}</u>.
            </p>
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""
