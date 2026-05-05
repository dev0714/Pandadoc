# MeanKat Café — Admin Panel

File: `Websites/Meankatcafe/app/admin/admin-client.tsx`

## Sidebar tabs

| Tab ID        | Label        | Icon |
|---------------|--------------|------|
| `cats`        | Cats         | 🐾   |
| `menu-images` | Menu Photos  | 📸   |

The "Menu Items" tab was removed (commit e0f5bf0). The `AdminTab` type is `"cats" | "menu-images"`.

## Cats tab

- Upload form: name, category (resident / adoptable / dual), description, image
- `POST /api/admin/cats` (multipart)
- Lists cats grouped by category; built-in cats hidden via localStorage key `meankat_hidden_cat_ids`
- Delete: built-ins go to localStorage hidden list; uploaded cats call `DELETE /api/admin/cats/[id]`

## Menu Photos tab

- Upload form: `POST /api/admin/menu-images` (multipart)
- Lists all photos; built-ins labeled "Built-in" with a Delete button
- Deleting a built-in stores its ID in localStorage key `meankat_hidden_menu_images`
- Deleting an uploaded image calls `DELETE /api/admin/menu-images/[id]`

## Auth

- Session checked via `GET /api/auth/me`
- Login: `POST /api/auth/login`
- Logout: `POST /api/auth/logout`
- Gate: `session.isAdmin && session.isApproved`
