const productImageModules = import.meta.glob("../assets/Products/*", {
  eager: true,
  import: "default",
});

export function getProductImage(product) {
  const imageFilename = product?.image_filename;

  if (!imageFilename) {
    return null;
  }

  const match = Object.entries(productImageModules).find(([path]) =>
    path.endsWith(`/${imageFilename}`),
  );

  return match ? match[1] : null;
}
