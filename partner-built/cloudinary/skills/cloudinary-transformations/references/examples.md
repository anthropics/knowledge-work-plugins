# Cloudinary Transformation Examples

Complete examples of common transformation patterns with explanations.

## Basic Resizing

### Scale by Width (Maintain Aspect Ratio)
```
c_scale,w_400
```
Resizes to 400px wide, height adjusts automatically.

### Scale by Height (Maintain Aspect Ratio)
```
c_scale,h_300
```
Resizes to 300px tall, width adjusts automatically.

### Fill Exact Dimensions
```
c_fill,g_auto,h_300,w_400
```
Crops and resizes to exactly 400x300, focusing on the most interesting part.

### Fit Within Dimensions
```
c_fit,h_300,w_400
```
Fits entire image within 400x300 box without cropping.

### Limit Maximum Size
```
c_limit,w_1000
```
Only scales down if larger than 1000px, never upscales.

## Smart Cropping

### Auto Crop with Face Detection
```
c_fill,g_face,h_200,w_200
```
Creates 200x200 thumbnail centered on detected face.

### Auto Crop to Interesting Content
```
c_auto,g_auto,h_400,w_600
```
Automatically crops to the most interesting part of the image.

### Thumbnail with Multiple Faces
```
c_thumb,g_faces,h_150,w_150
```
Creates thumbnail including all detected faces.

## Optimization

### Basic Optimization
```
f_auto/q_auto
```
Automatically selects best format (WebP, AVIF, etc.) and quality.

### High-Quality Optimization
```
f_auto/q_auto:best
```
Higher quality automatic optimization.

### Economy Optimization
```
f_auto/q_auto:eco
```
More aggressive compression for smaller files.

### Retina Display
```
c_scale,w_400/f_auto/q_auto/dpr_auto
```
Automatically serves 2x or 3x resolution for high-DPI displays.

**Note:** `dpr_auto` only works on Chromium-based browsers (Chrome, Edge, Opera, Samsung Internet) with Client Hints enabled. Falls back to `dpr_1.0` otherwise. For broader browser support, consider using explicit DPR values (e.g., `dpr_2.0`) or JavaScript-based responsive solutions.

## Effects

### Grayscale
```
e_grayscale/f_auto/q_auto
```

### Sepia Tone
```
e_sepia/f_auto/q_auto
```

### Blur
```
e_blur:800/f_auto/q_auto
```
Blur strength from 1-2000.

### Sharpen
```
e_sharpen:100/f_auto/q_auto
```

### Cartoonify
```
e_cartoonify/f_auto/q_auto
```

### Pixelate Faces
```
e_pixelate_faces:20/f_auto/q_auto
```

### Background Removal
```
e_background_removal/f_png
```
Removes background, use PNG to preserve transparency.

### Colorize
```
co_rgb:0044ff,e_colorize:40/f_auto/q_auto
```
Colorize with blue at 40% strength. Note: `co_` is a qualifier.

## Overlays

### Simple Logo Overlay
```
l_logo/c_scale,w_100/fl_layer_apply,g_north_west,x_10,y_10/f_auto/q_auto
```
Places 100px wide logo in top-left corner with 10px margins.

### Semi-Transparent Watermark
```
l_watermark/c_scale,fl_relative,o_40,w_0.25/fl_layer_apply,g_south_east,x_20,y_20/f_auto/q_auto
```
Places watermark at 25% of image width, 40% opacity, bottom-right with 20px margins.

### Text Overlay
```
co_white,l_text:Arial_60_bold:Hello%20World/fl_layer_apply,g_center/f_auto/q_auto
```
White text, 60px Arial Bold, centered.

### Text with Background
```
b_black,co_white,l_text:Arial_40:Sale/fl_layer_apply,g_north,y_50/f_auto/q_auto
```
White text on black background at top.

### Multiple Overlays
```
l_logo/c_scale,w_80/fl_layer_apply,g_north_west,x_10,y_10/l_badge/c_scale,w_60/fl_layer_apply,g_north_east,x_10,y_10/f_auto/q_auto
```
Logo in top-left, badge in top-right.

## Borders & Shapes

### Rounded Corners
```
c_fill,h_400,w_600/r_20/f_auto/q_auto
```
20px rounded corners.

### Circle
```
c_fill,h_300,w_300/r_max/f_auto/q_auto
```
Perfect circle (requires square dimensions).

### Border
```
bo_5px_solid_black/f_auto/q_auto
```
5px solid black border.

### Border with Rounded Corners
```
c_fill,h_400,w_600/bo_5px_solid_rgb:0066ff,r_20/f_png/q_auto
```
Blue border following rounded corners. Note: border and radius in same component.

### Outline for Transparent Images
```
co_rgb:0066ff,e_outline:outer:15:200/f_png
```
15px blue outline at 200 opacity for images with transparency.

## Background Colors

### Pad with Background
```
c_pad,b_lightblue,h_400,w_600/f_auto/q_auto
```
Pads image to 600x400 with light blue background.

### Background After Removal
```
e_background_removal/b_lightblue,c_pad,w_1.0/f_png
```
Removes background, then adds light blue. Note: background as qualifier with pad.

### Named Colors
```
c_pad,b_white,h_400,w_600/f_auto/q_auto
```
Common named colors: white, black, red, blue, green, yellow, etc.

### RGB Colors
```
c_pad,b_rgb:ff6600,h_400,w_600/f_auto/q_auto
```
Custom RGB color.

## Rotation & Flips

### Rotate 90 Degrees
```
a_90/f_auto/q_auto
```

### Rotate Custom Angle
```
a_-15/f_auto/q_auto
```
Rotates -15 degrees.

### Horizontal Flip
```
a_hflip/f_auto/q_auto
```

### Vertical Flip
```
a_vflip/f_auto/q_auto
```

### Rotate and Crop
```
a_45/c_fill,h_400,w_600/f_auto/q_auto
```
Rotates first, then crops to dimensions.

## Variables

### Square Dimensions
```
$size_300/c_fill,h_$size,w_$size/r_max/f_auto/q_auto
```
Creates 300x300 circle using variable.

### Reusable Color
```
$brand_!0066ff!/bo_5px_solid_rgb:$brand,c_fill,h_400,w_600/co_rgb:$brand,l_text:Arial_40:Brand/fl_layer_apply,g_south/f_auto/q_auto
```
Uses brand color for border and text.

### Template with Multiple Variables
```
$width_800,$height_600,$color_!blue!/b_$color,c_pad,h_$height,w_$width/f_auto/q_auto
```
Template for padded images with custom dimensions and color.

### Date Variable in Text
```
$date_25/co_white,l_text:Arial_60:Day%20$(date)/fl_layer_apply,g_center/f_auto/q_auto
```
Displays "Day 25" using variable.

## Conditionals

### Resize Large Images Only
```
if_w_gt_1000/c_scale,w_1000/if_end/f_auto/q_auto
```
Only resizes if width exceeds 1000px.

### Different Crop for Portrait vs Landscape
```
if_ar_gt_1.0/c_fill,h_400,w_600/if_else/c_fill,h_600,w_400/if_end/f_auto/q_auto
```
Landscape gets 600x400, portrait gets 400x600.

### Add Badge to Sale Items
```
if_!sale!_in_tags/l_sale_badge/c_scale,w_100/fl_layer_apply,g_north_east,x_10,y_10/if_end/f_auto/q_auto
```
Only adds sale badge if "sale" tag exists.

### Quality Based on Dimensions
```
if_w_gt_2000/q_90/if_else/q_auto/if_end/f_auto
```
Higher quality for large images.

### Multiple Conditions
```
if_w_gt_800_and_h_gt_600/c_fill,h_600,w_800/if_else/c_fit,h_600,w_800/if_end/f_auto/q_auto
```
Fill if large enough, otherwise fit.

## Complex Chained Transformations

### Avatar Pipeline
```
c_thumb,g_face,h_400,w_400/e_improve/r_max/bo_3px_solid_white/f_auto/q_auto
```
1. Crop to face (400x400)
2. Enhance quality
3. Make circular
4. Add white border
5. Optimize

### Product Image Pipeline
```
e_background_removal/c_pad,b_white,h_800,w_800/l_watermark/c_scale,fl_relative,o_30,w_0.2/fl_layer_apply,g_south_east,x_30,y_30/f_auto/q_auto
```
1. Remove background
2. Pad to 800x800 with white
3. Add watermark (20% width, 30% opacity)
4. Position bottom-right
5. Optimize

### Social Media Post
```
c_fill,g_auto,h_630,w_1200/co_white,l_text:Arial_80_bold:Breaking%20News/b_black,fl_layer_apply,g_north,y_50/co_yellow,l_text:Arial_40:Read%20More/fl_layer_apply,g_south,y_50/f_auto/q_auto
```
1. Crop to 1200x630 (Facebook/Twitter size)
2. Add bold white heading on black at top
3. Add yellow call-to-action at bottom
4. Optimize

### Before/After Comparison
```
c_fill,h_400,w_300/l_same_image/c_fill,e_grayscale,h_400,w_300/fl_layer_apply,fl_splice,g_east/f_auto/q_auto
```
Creates side-by-side comparison with grayscale version.

## Video Transformations

### Video Thumbnail
```
c_fill,g_auto,h_360,w_640/f_jpg/q_auto
```
Extracts frame as thumbnail.

### Video at Specific Time
```
c_fill,g_auto,h_360,so_5.0,w_640/f_jpg/q_auto
```
Thumbnail from 5 seconds in (`so_` = start offset).

### Video Resize
```
c_scale,w_720/f_auto/q_auto
```
Resizes video to 720px wide.

### Video with Overlay
```
l_logo/c_scale,w_100/fl_layer_apply,g_north_west,x_10,y_10/f_auto/q_auto
```
Adds logo throughout video.

## Responsive Images

### Automatic Breakpoints
```
c_fill,g_auto,w_auto:breakpoints/f_auto/q_auto/dpr_auto
```
Cloudinary generates optimal breakpoints.

**Note:** Both `w_auto` and `dpr_auto` require Client Hints and only work on Chromium-based browsers. Without Client Hints support, `w_auto` is ignored and `dpr_auto` falls back to `dpr_1.0`.

### Specific Breakpoints
```
c_fill,g_auto,w_auto:100:1600:80/f_auto/q_auto
```
Breakpoints from 100px to 1600px in 80px increments.

**Note:** `w_auto` requires Client Hints and only works on Chromium-based browsers.

### Art Direction
```
if_ar_gt_1.5/c_fill,h_400,w_800/if_else/c_fill,h_800,w_400/if_end/f_auto/q_auto
```
Different crops for different aspect ratios.

## Advanced Patterns

### Dynamic Text from Metadata
```
$title_!md:title!/co_white,l_text:Arial_50:$(title)/fl_layer_apply,g_north,y_30/f_auto/q_auto
```
Overlays text from asset metadata.

### Conditional Watermark
```
if_!premium!_nin_tags/l_watermark/c_scale,fl_relative,o_50,w_0.3/fl_layer_apply,g_center/if_end/f_auto/q_auto
```
Only watermarks non-premium images.

### Smart Crop with Fallback
```
c_fill,g_auto:subject,h_400,w_600/f_auto/q_auto
```
Tries to detect main subject, falls back to general auto.

### Aspect Ratio Preservation
```
c_fill,ar_16:9,w_800/f_auto/q_auto
```
Maintains 16:9 aspect ratio at 800px wide.

### Named Transformation
```
t_thumbnail/f_auto/q_auto
```
References a named transformation that's been defined for this product environment.

## Additional Crop Modes

### Limit Fill (c_lfill)
```
c_lfill,g_auto,h_400,w_600/f_auto/q_auto
```
Same as fill but only scales down, never upscales.

### Fill with Padding (c_fill_pad)
```
c_fill_pad,g_auto,h_400,w_600/f_auto/q_auto
```
Fills dimensions with smart crop, adds padding if needed. Requires `g_auto`.

### Auto with Padding (c_auto_pad)
```
c_auto_pad,g_auto,h_400,w_600/f_auto/q_auto
```
Automatically determines best crop, adds padding if needed. Requires `g_auto`.

### Minimum Fit (c_mfit)
```
c_mfit,h_400,w_600/f_auto/q_auto
```
Scales up only (opposite of c_limit).

### Imagga Smart Crop
```
c_imagga_crop,g_auto,h_400,w_600/f_auto/q_auto
```
Uses Imagga's smart cropping algorithm.

## Advanced Gravity Options

### Advanced Eyes Detection
```
c_fill,g_adv_eyes,h_300,w_300/f_auto/q_auto
```
Focuses on eyes for precise face cropping.

### Multiple Faces
```
c_fill,g_faces,h_400,w_600/f_auto/q_auto
```
Includes all detected faces in the crop.

### XY Center with Offsets
```
c_crop,g_xy_center,h_400,w_600,x_100,y_50/f_auto/q_auto
```
Centers crop at specific coordinates with offsets.

## Flags and Special Options

### Progressive Loading
```
c_scale,w_800/fl_progressive/f_jpg/q_auto
```
Delivers progressive JPEG for better perceived loading.

### Lossy Conversion
```
c_scale,w_800/fl_lossy/f_png/q_auto
```
Delivers lossy PNG for smaller file size.

### Force Download
```
c_scale,w_800/fl_attachment:my-image/f_auto/q_auto
```
Forces browser to download instead of display.

### Preserve Transparency
```
c_scale,w_800/fl_preserve_transparency/f_png
```
Ensures transparency is maintained during transformations.

### No Overflow
```
c_scale,w_2000/fl_no_overflow/f_auto/q_auto
```
Prevents upscaling beyond original dimensions.

### Immutable Cache
```
c_scale,w_800/fl_immutable_cache/f_auto/q_auto
```
Enables aggressive CDN caching.

### Region Relative Overlays
```
c_crop,h_400,w_600/l_badge/c_scale,fl_region_relative,w_0.3/fl_layer_apply,g_north_east/f_auto/q_auto
```
Sizes overlay relative to cropped region, not original image.

## Arithmetic Transformations

### Division
```
c_scale,w_div_2/f_auto/q_auto
```
Divides width by 2.

### Multiplication
```
c_scale,w_mul_1.5/f_auto/q_auto
```
Multiplies width by 1.5.

### Addition
```
c_crop,h_add_100,w_800/f_auto/q_auto
```
Adds 100 pixels to height.

### Subtraction
```
c_crop,h_sub_50,w_800/f_auto/q_auto
```
Subtracts 50 pixels from height.

### Using Initial Dimensions
```
c_scale,w_iw_div_2/f_auto/q_auto
```
Sets width to half of initial width (`iw` = initial width).

### Aspect Ratio Calculations
```
c_scale,w_800,h_800_div_ar/f_auto/q_auto
```
Calculates height based on aspect ratio.

## Context and Metadata Conditionals

### Context-Based Conditional
```
if_ctx:!category!_eq_!featured!/l_featured_badge/fl_layer_apply,g_north_east/if_end/f_auto/q_auto
```
Adds badge if context category equals "featured".

### Metadata Range Conditional
```
if_md:!price!_gt_100/l_premium_badge/fl_layer_apply,g_north_west/if_end/f_auto/q_auto
```
Adds premium badge if metadata price > 100.

### Multiple Metadata Conditions
```
if_md:!stock!_gt_0_and_md:!featured!_eq_!true!/e_saturation:50/if_end/f_auto/q_auto
```
Increases saturation if in stock AND featured.

## Advanced Text Overlays

### Text with Stroke
```
co_white,l_text:Arial_60_bold_stroke:Hello/fl_layer_apply,g_center/f_auto/q_auto
```
White text with stroke outline.

### Text with Letter Spacing
```
co_black,l_text:Arial_40_letter_spacing_10:SPACED/fl_layer_apply,g_center/f_auto/q_auto
```
Text with 10px letter spacing.

### Text with Line Spacing
```
co_black,l_text:Arial_40_line_spacing_20:Line%20One%0ALine%20Two/fl_layer_apply,g_center/f_auto/q_auto
```
Multi-line text with custom line spacing.

### Text with Border
```
bo_5px_solid_black,co_white,l_text:Arial_50:Bordered/fl_layer_apply,g_center/f_auto/q_auto
```
Text with border.

## Advanced Color Transformations

### Replace Color
```
e_replace_color:blue:50:white/f_auto/q_auto
```
Replaces blue colors (within 50 tolerance) with white.

### Tint
```
co_rgb:ff0000,e_tint:50/f_auto/q_auto
```
Applies 50% red tint.

### Contrast and Brightness
```
e_brightness:30/e_contrast:20/f_auto/q_auto
```
Increases brightness by 30 and contrast by 20.

### Saturation
```
e_saturation:50/f_auto/q_auto
```
Increases saturation by 50.

### Hue Shift
```
e_hue:40/f_auto/q_auto
```
Shifts hue by 40 degrees.

## Generative AI Examples

### Generative Fill
```
c_pad,ar_16:9,b_gen_fill,w_1200/f_auto/q_auto
```
Uses AI to fill padded areas with generated content.

### Generative Replace
```
e_gen_replace:from_dog;to_cat/f_auto/q_auto
```
Replaces dogs with cats using AI.

### Generative Restore
```
e_gen_restore/f_auto/q_auto
```
Restores and enhances old or low-quality images.

### Generative Recolor
```
e_gen_recolor:prompt_golden%20hour%20lighting/f_auto/q_auto
```
Recolors image based on text prompt.

## Quality Variations

### Quality with Chroma Subsampling
```
c_scale,w_800/f_jpg/q_80:420
```
JPEG quality 80 with 4:2:0 chroma subsampling.

### Quality Range
```
c_scale,w_800/f_auto/q_auto:low
```
Automatic quality with low setting for smaller files.

## DPR and Responsive

**Important:** `dpr_auto` and `w_auto` parameters only work on Chromium-based browsers (Chrome, Edge, Opera, Samsung Internet) with Client Hints enabled. They do NOT work inside named transformations. For broader browser support, see the [Responsive Images documentation](https://cloudinary.com/documentation/responsive_images).

### Specific DPR
```
c_scale,w_400/dpr_2.0/f_auto/q_auto
```
Delivers 800px image for 2x displays. Explicit DPR values work in all browsers.

### Auto Breakpoints
```
c_fill,g_auto,w_auto:breakpoints/f_auto/q_auto
```
Cloudinary generates optimal responsive breakpoints. Requires Client Hints support.

### Breakpoints with Range
```
c_fill,g_auto,w_auto:100:1600:80/f_auto/q_auto
```
Breakpoints from 100px to 1600px in 80px steps. Requires Client Hints support.

## Fetch Delivery Type

### Fetch Remote Image
```
https://res.cloudinary.com/demo/image/fetch/c_scale,w_400/f_auto/q_auto/https://example.com/image.jpg
```
Fetches and transforms remote image.

### Fetch with Signature
```
https://res.cloudinary.com/demo/image/fetch/s--signature--/c_scale,w_400/f_auto/q_auto/https://example.com/image.jpg
```
Fetches remote image with signed URL for security.
