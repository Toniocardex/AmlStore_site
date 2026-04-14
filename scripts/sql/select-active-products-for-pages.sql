SELECT
  id,
  slug,
  title_it,
  title_en,
  title_de,
  title_fr,
  title_es,
  description_it,
  description_en,
  description_de,
  description_fr,
  description_es,
  price_cents,
  currency,
  fulfillment,
  cover_image
FROM products
WHERE active = 1
ORDER BY COALESCE(sort_order, 2147483647), id;
