# Home-assistant-Solax-cloud
Solax cloud integration for home assistant


todo things:
1. Add labels to the config flow input fields, Don't know why these are not shown.
2. Get inverter type and based on model add the correct sensor to the integration
3. Translation
4. 

goal:
add integration to the official home assistant integration list.

usage:
1. Use the PocketLAN or PocketWiFi serial number, NOT the inverter serial number.
2. Obtain Token from the Solax Cloud website
   Old interface:
   Service -> API -> API: Real-time display -> TokenID
   New interface:
   Support -> Third-party ecology -> API: Real-Time Display -> TokenID


Installation:
Add repository URL to custom repository in hacs
See: https://hacs.xyz/docs/faq/custom_repositories/
