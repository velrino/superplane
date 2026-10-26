# Notion integration evidence

These original screenshots record manual validation in a restricted Notion workspace. They cover connection setup, page creation, linked outputs, pagination, empty results, and an expected API error.

The documentation was later shortened. These captures belong to the original validation, not a new test run of the documentation revision.

Screenshot 10 uses a page ID as a data source ID. The expected 404 stops execution before page creation.

<table>
  <tr>
    <td width="100%" valign="top">
      <strong>01. Restricted sandbox access</strong><br />
      The internal Notion connection has access to the dedicated QA sandbox.<br /><br />
      <img width="100%" alt="01-notion-sandbox-access" src="https://github.com/user-attachments/assets/831c47d3-351d-4546-bea6-20afcabc119e" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>02. Connected Notion integration</strong><br />
      SuperPlane verifies the Notion connection and shows it as ready to use.<br /><br />
      <img width="100%" alt="02-superplane-notion-connected" src="https://github.com/user-attachments/assets/a001062a-5d61-43b6-8e8e-a1925d07bd7b" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>03. Created incident runbook</strong><br />
      The workflow creates an incident runbook with an English heading, explanatory text, and numbered instructions.<br /><br />
      <img width="100%" alt="03-notion-created-runbook" src="https://github.com/user-attachments/assets/46789710-c769-4f35-a092-7728bd070b1c" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>04. Created task with custom properties</strong><br />
      The workflow creates a data source entry using the custom Task title property and sets the Verified checkbox.<br /><br />
      <img width="100%" alt="04-notion-created-database-entry" src="https://github.com/user-attachments/assets/ad942755-d5db-4160-ac7f-eb498e3ef89d" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>05. Task linked to the previous output</strong><br />
      The task includes the runbook URL returned by the previous action, demonstrating output expressions between workflow steps.<br /><br />
      <img width="100%" alt="05-notion-task-linked-output" src="https://github.com/user-attachments/assets/9d818dd3-519c-44ab-bd4b-44df14004893" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>06. Created page details in SuperPlane</strong><br />
      The execution summary shows the created page ID, title, and a direct link to open it in Notion.<br /><br />
      <img width="100%" alt="06-superplane-created-page-details" src="https://github.com/user-attachments/assets/7edb99ad-b1d1-4463-aefc-19bc286bc06f" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>07. Successful workflow execution</strong><br />
      The complete workflow passes: it creates a runbook and task, then searches shared content and retrieves the next page of results.<br /><br />
      <img width="100%" alt="07-superplane-workflow-passed" src="https://github.com/user-attachments/assets/5f62dec2-9710-4a3b-a86a-c8f4a7122f1f" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>08. Search pagination</strong><br />
      The first search returns one result and indicates that more results are available through pagination.<br /><br />
      <img width="100%" alt="08-superplane-search-pagination" src="https://github.com/user-attachments/assets/813dc4aa-a515-4ac9-8927-51f881b83428" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>09. Successful search with no results</strong><br />
      A search with no matching titles returns zero results and completes successfully.<br /><br />
      <img width="100%" alt="09-superplane-empty-search" src="https://github.com/user-attachments/assets/aa63eadd-2efb-405d-9e1d-4811b2527a7b" />
    </td>
  </tr>
  <tr>
    <td width="100%" valign="top">
      <strong>10. Expected error for an invalid data source</strong><br />
      A page ID is intentionally supplied as a data source ID. The expected 404 appears in SuperPlane before page creation.<br /><br />
      <img width="100%" alt="10-superplane-expected-notion-error" src="https://github.com/user-attachments/assets/21271566-118e-4d67-863b-866852dc47cf" />
    </td>
  </tr>
</table>
