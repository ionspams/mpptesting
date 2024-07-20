Custom Bitlinks
These endpoints are for updating custom Bitlinks only. Custom Bitlinks have both a BSD and a customized back-half (e.g., yourcompany.com/yourcampaign). If a link begins with the bit.ly domain or ends with an auto-generated random string it is not a custom Bitlink.

Add Custom Bitlink
 /v4/custom_bitlinks
Add a keyword (or "custom back-half") to a Bitlink with a Custom Domain (domains must match). This endpoint can also be used for initial redirects to a link.

Request Body Schema
custom_bitlinkstring
bitlink_idstring
Request

cURL
curl \
-H 'Authorization: Bearer {TOKEN}' \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "custom_bitlink": "chauncey.ly/documentation",
  "bitlink_id": "chauncey.ly/1234abcd"
}' \
https://api-ssl.bitly.com/v4/custom_bitlinks
Response

200 SUCCESS
{
  "custom_bitlink": "string",
  "bitlink": {
    "references": { "any" },
    "link": "string",
    "id": "string",
    "long_url": "string",
    "title": "string",
    "archived": "boolean",
    "created_at": "string",
    "created_by": "string",
    "client_id": "string",
    "custom_bitlinks": [
      "string"
    ],
    "tags": [
      "string"
    ],
    "launchpad_ids": [
      "string"
    ],
    "deeplinks": [
      {
        "guid": "string",
        "bitlink": "string",
        "app_uri_path": "string",
        "install_url": "string",
        "app_guid": "string",
        "os": "string",
        "install_type": "string",
        "created": "string",
        "modified": "string",
        "brand_guid": "string"
      }
    ],
    "campaign_ids": [
      "string"
    ]
  },
  "bitlink_history": [
    {
      "uuid": "string",
      "group_guid": "string",
      "keyword": "string",
      "bsd": "string",
      "hash": "string",
      "login": "string",
      "long_url": "string",
      "created": "string",
      "first_created": "string",
      "deactivated": "string",
      "is_active": "boolean"
    }
  ]
}
Update Custom Bitlink
 /v4/custom_bitlinks/{custom_bitlink}
Move a keyword (or custom back-half) to a different Bitlink (domains must match).

Path Parameters
custom_bitlinkstringRequired
A Custom Bitlink made of the domain and keyword
Request Body Schema
bitlink_idstring
Request

cURL
curl \
-H 'Authorization: Bearer {TOKEN}' \
-H 'Content-Type: application/json' \
-X PATCH \
-d '{
  "bitlink_id": "chauncey.ly/1234abcd"
}' \
https://api-ssl.bitly.com/v4/custom_bitlinks/chauncey.ly/chauncey
Response

200 SUCCESS
{
  "custom_bitlink": "string",
  "bitlink": {
    "references": { "any" },
    "link": "string",
    "id": "string",
    "long_url": "string",
    "title": "string",
    "archived": "boolean",
    "created_at": "string",
    "created_by": "string",
    "client_id": "string",
    "custom_bitlinks": [
      "string"
    ],
    "tags": [
      "string"
    ],
    "launchpad_ids": [
      "string"
    ],
    "deeplinks": [
      {
        "guid": "string",
        "bitlink": "string",
        "app_uri_path": "string",
        "install_url": "string",
        "app_guid": "string",
        "os": "string",
        "install_type": "string",
        "created": "string",
        "modified": "string",
        "brand_guid": "string"
      }
    ],
    "campaign_ids": [
      "string"
    ]
  },
  "bitlink_history": [
    {
      "uuid": "string",
      "group_guid": "string",
      "keyword": "string",
      "bsd": "string",
      "hash": "string",
      "login": "string",
      "long_url": "string",
      "created": "string",
      "first_created": "string",
      "deactivated": "string",
      "is_active": "boolean"
    }
  ]
}
