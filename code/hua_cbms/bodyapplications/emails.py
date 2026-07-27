SEC_APPLICATION_NOTIFICATION_SUBJECT = "New Application to a Collective Body / Νέο Αίτημα προς ένα Συλλογικό Όργανο"

SEC_APPLICATION_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:white; padding:30px; border-radius:6px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">New Application submitted</h2>

            <p>Hello,</p>

            <p>The applicant with the following details:</p>

            <table cellpadding="6" cellspacing="0" style="margin-bottom:15px;">
              <tr>
                <td><strong>First name:</strong></td>
                <td>{first_name}</td>
              </tr>
              <tr>
                <td><strong>Last name:</strong></td>
                <td>{last_name}</td>
              </tr>
              <tr>
                <td><strong>Email:</strong></td>
                <td>{email}</td>
              </tr>
            </table>

            <p>
              has successfully submitted an application to the collective body <strong>{collective_body_title_en}</strong>.
            </p>

            <p>
              <strong>Application details:</strong>
            </p>

            <p style="background-color:#f8f9fa; padding:12px; border-radius:4px; border:1px solid #e0e0e0;">
              Request subject: {request_subject}<br>
              Description: {description}
            </p>

            <p>
              Please log in to the platform in order to review the request and, 
              if required, link it to a relevant collective body subject.
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:20px 0;">
              <tr>
                <td align="center" style="background:#1a73e8; padding:12px 22px; border-radius:4px;">
                  <a href="{url}" style="color:white; text-decoration:none; font-weight:bold;">
                    View Application
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

            <h2 style="margin-top:0; color:#1a73e8;">Υποβλήθηκε νέα αίτηση</h2>

            <p>Γειά σας,</p>

            <p>Ο αιτών με τα παρακάτω στοιχεία:</p>

            <table cellpadding="6" cellspacing="0" style="margin-bottom:15px;">
              <tr>
                <td><strong>Όνομα:</strong></td>
                <td>{first_name}</td>
              </tr>
              <tr>
                <td><strong>Επώνυμο:</strong></td>
                <td>{last_name}</td>
              </tr>
              <tr>
                <td><strong>Email:</strong></td>
                <td>{email}</td>
              </tr>
            </table>

            <p>
              έχει υποβάλει επιτυχώς αίτηση στο συλλογικό όργανο <strong>{collective_body_title_gr}</strong>.
            </p>

            <p>
              <strong>Στοιχεία αίτησης:</strong>
            </p>

            <p style="background-color:#f8f9fa; padding:12px; border-radius:4px; border:1px solid #e0e0e0;">
              Θέμα αιτήματος: {request_subject}<br>
              Περιγραφή: {description}
            </p>

            <p>
              Παρακαλούμε συνδεθείτε στην πλατφόρμα για να εξετάσετε το αίτημα και, εφόσον απαιτείται,
              να το συνδέσετε με σχετικό θέμα συλλογικού οργάνου.
            </p>

            <table cellpadding="0" cellspacing="0" style="margin:20px 0;">
              <tr>
                <td align="center" style="background:#1a73e8; padding:12px 22px; border-radius:4px;">
                  <a href="{url}" style="color:white; text-decoration:none; font-weight:bold;">
                    Προβολή Αιτήματος
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

SEC_APPLICATION_UPDATE_NOTIFICATION_SUBJECT = "Application update / Ενημέρωση αιτήματος"

SEC_APPLICATION_UPDATE_NOTIFICATION_BODY = """
<table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0" style="background:white; padding:30px; border-radius:6px; color:#222; line-height:1.6;">

        <!-- English Section -->
        <tr>
          <td>
            <h2 style="margin-top:0; color:#1a73e8;">Application updated</h2>

            <p>Hello,</p>

            <p>The application concerning user <strong>{applicant_username}</strong>, has been updated.</p>

            <p>
              Log in to the platform for more details.
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

            <h2 style="margin-top:0; color:#1a73e8;">Αίτημα ενημερώθηκε</h2>

            <p>Γειά σας,</p>

            <p>Η αίτηση που αφορά τον χρήστη <strong>{applicant_username}</strong> έχει ενημερωθεί.</p>

            <p>
              Συνδεθείτε στην πλατφόρμα για περισσότερες λεπτομέρειες.
            </p>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""
