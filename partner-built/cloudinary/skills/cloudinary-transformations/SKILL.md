---
name: cloudinary-transformations
description: Create and debug Cloudinary transformation URLs from natural language instructions. Use when building Cloudinary delivery URLs, applying image/video transformations, optimizing media, or debugging transformation syntax errors.
---

# Cloudinary Transformation Rules

This skill helps you create valid Cloudinary transformation URLs from natural language instructions and debug transformation issues.

## When to Use This Skill

- Building Cloudinary delivery/transformation URLs
- Converting natural language requests to transformation syntax
- Debugging transformation URLs that aren't working
- Optimizing images or videos with Cloudinary
- Applying effects, overlays, resizing, or cropping

## Gathering Requirements

Before generating a transformation URL, if not already specified, clarify these details based on the user's request:

### For Resize/Crop Requests
**Required:**
- At least one dimension (width OR height)
- Crop behavior if both dimensions specified (fill, pad, scale, limit, etc.)

**Clarify:**
- Focal point/gravity (especially for cropping): Face detection? Center? Smart auto-detection?
- Maintain aspect ratio? (if only one dimension, this is automatic)

**Example questions:**
- "What dimensions do you need? (width and/or height)"
- "Should this fill the space (may crop) or fit within it (no cropping)?"
- "Any important focal point? (faces, center, specific area)"

### For AI Transformation Requests
**Background removal:**
- Output format needs (PNG for transparency vs JPG with solid background)
- What to do with transparent area (keep transparent, add color, or gen_fill)

**Generative fill:**
- Target dimensions or aspect ratio
- How much extension needed

**Generative replace:**
- What object to replace (from)
- What to replace it with (to)
- Preserve original shape? (for clothing/objects)

**Generative remove:**
- What object(s) to remove
- Remove all instances or just one?

**Generative background replace:**
- Describe desired background (or use auto-generation)
- Need reproducibility? (consider seed parameter)

### For Video Transformation Requests
**Trimming:**
- Start and end time, or duration
- Seconds or percentage of video

**Codec/format:**
- Output format needs (MP4, WebM, etc.)
- Quality requirements (use `vc_auto` if unsure)

**Audio:**
- Keep or remove audio track
- If for autoplay, suggest removing audio (`ac_none`)

### Always Recommend
Unless user specifies otherwise:
- Add `f_auto/q_auto` for automatic format/quality optimization
- Use `g_auto` for smart cropping when filling dimensions
- Consider cost for AI transformations (inform user of transformation credits)

## Quick Reference

### URL Structure

```
https://res.cloudinary.com/<cloud_name>/<asset_type>/<delivery_type>/<transformations>/<version>/<public_id>.<ext>
```

**Key Rules:**
- Commas (`,`) separate parameters **within** a component
- Slashes (`/`) separate components **between** transformations
- Each component acts on the output of the previous one

### Parameter Types

**Action parameters**: Perform transformations (one action per component: each action transformation should be separated by a slash)
**Qualifier parameters**: Modify action behavior (in the same component as the action, using commas as separators)

Check the [Transformation Reference](https://cloudinary.com/documentation/transformation_reference.md) to determine if a parameter is an action or qualifier.

## Core Transformations

### Resize & Crop

**Dimension value formats:**
- **Whole numbers** (e.g., `w_400`, `h_300`) = pixels
- **Decimal values** (e.g., `w_0.5`, `h_1.0`) = percentage of original dimensions (0.5 = 50%, 1.0 = 100%)

**Choosing the right crop mode:**

Use **`c_scale`** when:
- Resizing while maintaining original aspect ratio
- Specify only ONE dimension (width OR height)
- No cropping needed
- The user intentionally wants to stretch or squash an image by changing the aspect ratio

Use **`c_fill`** when:
- Must fit exact dimensions (e.g., thumbnail grid, fixed layout)
- Okay to crop parts of image
- Combine with `g_auto` for smart cropping, or `g_face` for portraits

Use **`c_fit`** when:
- Image must fit within dimensions without cropping
- Okay to have empty space
- Maintaining full image content is critical

Use **`c_pad`** when:
- Must fit exact dimensions without cropping
- Need to fill empty space with background color/blur/AI-generated pixels
- Use with `b_<color>` or `b_auto` (blurred background) or `b_gen_fill`

Use **`c_limit`** when:
- Set maximum dimensions but don't upscale small images
- Preserving original quality of small images matters

Use **`c_thumb`** when:
- Creating thumbnails (typically avatars)
- Use with `g_face` for face-centered crops

Use **`c_auto`** when:
- Cloudinary should intelligently crop to interesting content
- Combine with `g_auto` for best results
- Good for dynamic content where focal point varies

**Examples:**
```
c_scale,w_400                      # Resize width to 400px, maintain aspect ratio
c_scale,w_0.5                      # Resize to 50% of original width
c_fill,g_auto,h_300,w_400          # Fill 400x300px dimensions, smart crop
c_fit,h_300,w_400                  # Fit within dimensions, no crop
c_pad,b_white,h_300,w_400          # Pad to exact size with white background
c_pad,w_1.0                        # Pad to original width (100%)
c_limit,w_1000                     # Limit max width, no upscale
c_thumb,g_face,h_150,w_150         # Face-centered square thumbnail
c_auto,g_auto,w_800                # Auto crop to interesting area
```

**Important**: Always specify a crop mode explicitly. Avoid using both dimensions with `c_scale` (will distort if aspect ratios don't match) - prefer one dimension to maintain aspect ratio.

### Gravity (Focal Point)

```
g_auto          # Smart detection (works with c_fill, c_lfill, c_crop, c_thumb, c_auto)
g_face          # Face detection
g_center        # Center position
g_north_west    # Compass positions
x_20,y_30       # Pixel offsets
x_0.8,y_0.2     # Percentage offsets (0.8 = 80%, 0.2 = 20%)
```

**Coordinate value formats (x, y):**
- **Integers** (e.g., `x_20`, `y_30`) = pixels
- **Float values** (e.g., `x_0.8`, `y_0.2`) = percentage in relation to 1.0 (0.8 = 80%, 0.2 = 20%)
- **Important**: When using x, y, h, and w together, use either integers or floats for all values. Do not mix types.

**Note**: `g_auto` does NOT work with `c_scale`, `c_fit`, `c_limit`, `c_pad`, or overlay positioning.

### Format & Quality

```
f_auto/q_auto           # Automatic optimization (best practice: separate components)
f_webp                  # Specific format
q_80                    # Quality level
dpr_auto                # Retina displays (see important notes below)
```

**Best Practice**: Format and quality parameters should be in separate components using `/`. While `f_auto,q_auto` works, separating them (e.g., `f_auto/q_auto`) is cleaner and more maintainable.

#### Important Notes About `dpr_auto`

`dpr_auto` automatically matches the Device Pixel Ratio (DPR) of the user's device, but has several important limitations:

**Browser Compatibility:**
- **Only works on Chromium-based browsers** (Chrome, Edge, Opera, Samsung Internet)
- Requires [Client Hints](https://cloudinary.com/documentation/responsive_server_side_client_hints) to be enabled
- If Client Hints aren't supported or available, the URL is treated as `dpr_1.0`

**Named Transformation Limitation:**
- ❌ **Does NOT work inside named transformations** (similar to `f_auto`)
- The client or CDN won't "see" `dpr_auto` when it's inside a named transformation
- ✅ Use `dpr_auto` directly in the URL, not within `t_<name>`

**To enable Client Hints**, add to your HTML `<head>` before any `<link>`, `<style>`, or `<script>` elements:
```html
<meta http-equiv="Accept-CH" content="DPR, Viewport-Width, Width">
<meta http-equiv="Delegate-CH" content="DPR https://res.cloudinary.com; Viewport-Width https://res.cloudinary.com; Width https://res.cloudinary.com">
```

**Alternative solutions** for better browser support:
- Use JavaScript-based responsive solutions (see [Responsive Images docs](https://cloudinary.com/documentation/responsive_images))
- Specify explicit DPR values (e.g., `dpr_2.0`) for high-resolution displays
- Use `w_auto` with Client Hints for automatic width-based responsiveness

For more details, see:
- [Responsive images using Client Hints](https://cloudinary.com/documentation/responsive_server_side_client_hints)
- [Responsive images overview](https://cloudinary.com/documentation/responsive_images)

### Effects

```
e_sepia                 # Sepia tone
e_grayscale             # Grayscale
e_blur:800              # Blur effect
e_sharpen               # Sharpen
e_cartoonify            # Cartoon effect
e_background_removal    # Remove background
co_rgb:0044ff,e_colorize:40  # Colorize (co_ is qualifier)
```

### Overlays & Underlays

```
l_logo/c_scale,w_100/fl_layer_apply,g_north_west,x_10,y_10
```

**Pattern:**
1. Declare layer: `l_<public_id>` or `u_<public_id>`
2. Transform layer: `/c_scale,w_100/` (optional)
3. Apply layer: `/fl_layer_apply,g_<position>,x_<offset>,y_<offset>`

**Text overlays:**
```
co_yellow,l_text:Arial_40:Hello%20World/fl_layer_apply,g_south
```
**Important**: Color (`co_`) is a qualifier — it must be in the **same component** as the text overlay declaration, not in a separate component.

### Borders & Rounding

```
r_20                    # Rounded corners
r_max                   # Circle (if square dimensions)
bo_5px_solid_black      # Border
```

**Important**: For borders that follow rounded corners, use border as qualifier in same component:
```
r_20,bo_5px_solid_rgb:0066ff
```

### Background Color

```
b_lightblue,c_pad,w_1.0    # Background with pad crop
b_gen_fill                 # AI-generated background fill
```

**Critical**: Use background as a qualifier with a pad crop, NOT in its own component when chaining transformations.

### Rotation & Flips

```
a_90                    # Rotate 90 degrees
a_-20                   # Rotate -20 degrees
a_hflip                 # Horizontal flip
a_vflip                 # Vertical flip
```

## Generative AI Transformations

Cloudinary's AI transformations solve common business challenges. **Proactively suggest these when appropriate:**

### Background Removal (`e_background_removal`)
**Cost:** 75 tx | **Use when:** Product images, portraits, preparing for overlays
**Value:** Professional product photos without manual editing

```
e_background_removal/f_png
```

### Generative Fill (`b_gen_fill`)
**Cost:** 50 tx | **Use when:** Changing aspect ratios without cropping, extending images
**Value:** Adapt one image to multiple formats without reshooting

```
c_pad,ar_16:9,b_gen_fill,w_1200/f_auto/q_auto
```

### Auto Enhance (`e_auto_enhance`)
**Cost:** 100 tx | **Use when:** Improving UGC quality, correcting lighting/exposure
**Value:** Professional-looking images without manual photo editing

```
e_auto_enhance/f_auto/q_auto
```

### Upscale (`e_upscale`)
**Cost:** 10-100 tx | **Use when:** Enlarging images without quality loss
**Value:** Use existing images at larger sizes for print or displays

```
e_upscale/c_scale,w_2000/f_auto/q_auto
```

### Generative Background Replace (`e_gen_background_replace`)
**Cost:** 230 tx | **Use when:** Replacing backgrounds with AI-generated environments
**Value:** Create contextual product imagery without photoshoots

```
e_gen_background_replace:prompt_modern office space/f_auto/q_auto
e_gen_background_replace:prompt_<text>;seed_<num>      # Use seed for reproducibility
```

**Key notes:**
- Auto-detects/preserves foreground on non-transparent images
- For transparent images, fills transparent area
- Not supported for animated/fetched images

### Generative Replace (`e_gen_replace`)
**Cost:** 120 tx | **Use when:** Swapping objects, A/B testing product variations
**Value:** Create product variations instantly without reshoots

```
e_gen_replace:from_shirt;to_cable knit sweater;preserve-geometry_true
e_gen_replace:from_<object>;to_<replacement>;multiple_true     # Replace all instances
```

**Key notes:**
- Use `preserve-geometry_true` to maintain shape (ideal for clothing)
- Don't use for faces, hands, or text
- Only works on non-transparent images

### Generative Restore (`e_gen_restore`)
**Cost:** 100 tx | **Use when:** Restoring old photos, fixing compression artifacts
**Value:** Revitalize low-quality or historical content at scale

```
e_gen_restore/f_auto/q_auto
```

**Key notes:** Removes artifacts, reduces noise, sharpens, recovers detail

### Generative Remove (`e_gen_remove`)
**Cost:** 50 tx | **Use when:** Removing unwanted objects, cleaning product photos
**Value:** Clean up images at scale without manual editing

```
e_gen_remove:prompt_the stick/f_auto/q_auto
e_gen_remove:prompt_goose;multiple_true                 # Remove all instances
e_gen_remove:prompt_(text;person)                       # Remove multiple types
```

**Key notes:** Parentheses syntax removes multiple different objects simultaneously

### When to Suggest AI Transformations

**Proactively recommend:**
- "Remove background" → `e_background_removal`
- "Replace background" → `e_gen_background_replace:prompt_<text>`
- "Change aspect ratio without cropping" → `b_gen_fill` with `c_pad`
- "Swap object/change color" → `e_gen_replace:from_<obj>;to_<new>`
- "Fix old photo/restore" → `e_gen_restore`
- "Remove object" → `e_gen_remove:prompt_<text>`
- "Improve quality" → `e_auto_enhance`
- "Make bigger" → `e_upscale`

**Powerful combinations:**
```
e_background_removal/e_gen_background_replace:prompt_modern office/f_auto/q_auto
e_gen_remove:prompt_price tag/e_background_removal/b_white,c_pad,w_1.0/e_auto_enhance/f_auto/q_auto
e_gen_restore/e_upscale/c_scale,w_2000/f_auto/q_auto
e_background_removal/b_gen_fill,c_pad,ar_16:9,w_1200/e_auto_enhance/f_auto/q_auto
```

## Video-Specific Transformations

### Video Codec (`vc_`)

```
vc_auto                        # Automatic codec selection (recommended)
vc_h264:high:4.1               # H.264 with profile and level
vc_h265, vc_vp8, vc_vp9, vc_av1  # Other codecs
vc_none                        # Remove video, keep audio only
```

**Key options:** h264 profiles (`baseline`, `main`, `high`), levels (`3.0`-`5.2`)

### Trimming Videos (`so_`, `eo_`, `du_`)

```
so_6.5                         # Start at 6.5 seconds
eo_10                          # End at 10 seconds
du_15                          # Duration of 15 seconds
so_10p, eo_90p, du_30p         # Percentage-based (0p-100p)
```

**Value formats:** Seconds (float) or percentage (`10p`)

### Audio Control (`ac_`)

```
ac_none                        # Remove audio track (for autoplay)
ac_aac, ac_mp3, ac_vorbis, ac_opus  # Audio codecs
```

### Frame Rate (`fps_`)

```
fps_30                         # Set FPS (ensures audio sync)
fps_20-25                      # FPS range
```

### Video Concatenation (`fl_splice`)

**Pattern:**
1. Declare: `fl_splice,l_video:<public_id>`
2. Transform overlay (optional)
3. Apply: `fl_layer_apply` (with `so_0` to splice at beginning)

```
c_fill,h_300,w_450/du_5/fl_splice,l_video:second_clip/c_fill,h_300,w_450/du_5/fl_layer_apply
```

**Important:** Both videos should be resized to matching dimensions before splicing

## Variables & Conditionals

### Variables

Use when values are reused or for template transformations.

```
$width_300/c_fill,h_$width,w_$width    # Declare and use
$date_12/l_text:Arial_40:$(date)/fl_layer_apply  # String variables use !text!
```

**Rules:**
- Variable names: alphanumeric only, must start with letter, NO underscores
- String assignment: `$var_!text value!`
- Reference: `$var` or `$(var)` in text

### Conditionals

```
if_w_gt_300/c_scale,w_300/if_end
if_!sale!_in_tags/l_sale_icon/fl_layer_apply/if_end
if_w_gt_300_and_h_gt_200/c_fill,h_200,w_300/if_else/c_pad,h_200,w_300/if_end
```

**Operators:**
- `eq`, `ne`, `lt`, `gt`, `lte`, `gte`
- `in`, `nin` (for tags)
- `and`, `or` (AND takes precedence)

**Conditions:**
- Dimensions: `if_w_gt_300`, `if_h_lte_200`
- Aspect ratio: `if_ar_gt_1.0`
- Tags: `if_!sale!_in_tags`
- Metadata: `if_md:!stock-level!_lt_50`

## Common Patterns

```
c_thumb,g_face,h_300,w_300/r_max/f_auto/q_auto              # Avatar
c_fit,w_1200/l_logo/c_scale,o_40,w_0.25/fl_layer_apply,g_south_east,x_20,y_20/f_auto/q_auto  # Watermark scaled to a quarter of its size
e_background_removal/b_lightblue,c_pad,w_1.0/f_png          # Background removal + color
co_yellow,l_text:Arial_60_bold:Hello/fl_layer_apply,g_north,y_50  # Text overlay
du_5/vc_auto/f_auto/q_auto                                   # 5-second video preview
ac_none/vc_h264/f_mp4/q_auto                                 # Silent video (autoplay)
```

## Self-Validation Checklist

**Before returning a transformation URL, verify:**

1. ✅ **URL structure is complete** (cloud_name, asset_type `/image/` or `/video/` or `/raw/`, delivery_type, public_id)
2. ✅ **Each component has only one action parameter** (e.g., one crop mode per component)
3. ✅ **Crop mode is explicit** (don't rely on defaults; avoid both dimensions with `c_scale`)
4. ✅ **Overlays end with `fl_layer_apply`** in separate component
5. ✅ **Text strings are URL-encoded** (spaces = `%20`, special chars encoded)
6. ✅ **Variable names follow rules** (alphanumeric, start with letter, no underscores)
7. ✅ **`g_auto` compatibility** (only works with `c_fill`, `c_lfill`, `c_crop`, `c_thumb`, `c_auto`)
8. ✅ **Background as qualifier** (use with pad crop: `b_color,c_pad,w_X`, not `/b_color/`)
9. ✅ **Format/quality at end** (prefer `f_auto/q_auto` as final components)

**Quick syntax check:**
- Commas separate parameters within a component: `c_fill,g_auto,w_400`
- Slashes separate components: `c_fill,w_400/f_auto/q_auto`
- Actions vs qualifiers: Only one action per component, qualifiers modify that action

See [references/debugging.md](references/debugging.md) for detailed examples of each check.

## Debugging Checklist

When a transformation isn't working:

1. **Verify URL structure**: Check that all required URL parts are present:
   - Cloud name: `/<cloud_name>/`
   - Asset type: `/image/` or `/video/` or `/raw/`
   - Delivery type: `/upload/` or `/fetch/` etc.
   - Public ID at the end
2. **Check the X-Cld-Error header**: Cloudinary reports errors in the `X-Cld-Error` HTTP response header
3. **Check parameter names** against [Transformation Reference](https://cloudinary.com/documentation/transformation_reference.md)
4. **Check crop mode**: Specify crop mode explicitly; avoid both dimensions with `c_scale` (causes distortion if aspect ratios don't match)
5. **Verify gravity compatibility**: `g_auto` doesn't work with `c_scale`, `c_fit`, `c_limit`, `c_pad`
6. **Check action vs qualifier**: Only one action per component, qualifiers in same component
7. **Verify overlay pattern**: Must end with `fl_layer_apply` component
8. **Check variable names**: No underscores, must start with letter
9. **Verify URL encoding**: Text overlays need URL-encoded strings (spaces = `%20`)
10. **Check auto parameters in named transformations**: `f_auto`, `dpr_auto`, and `w_auto` don't work inside named transformations - use them directly in URLs
11. **Verify Client Hints for `dpr_auto`/`w_auto`**: These only work on Chromium browsers with Client Hints enabled; fallback to `dpr_1.0` otherwise

### Checking X-Cld-Error Header

The `X-Cld-Error` header contains error details when a transformation fails. To check it:

**Using browser DevTools:**
1. Open Developer Tools (Network tab)
2. Request the transformation URL
3. Look for `X-Cld-Error` in Response Headers

**Using code (fetch the URL):**
```javascript
fetch('https://res.cloudinary.com/demo/image/upload/w_abc/sample.jpg')
  .then(response => {
    const error = response.headers.get('x-cld-error');
    if (error) {
      console.log('Cloudinary Error:', error);
    }
  });
```

**Common X-Cld-Error messages:**
- `Invalid width - abc` - Width parameter expects a number
- `Invalid transformation syntax` - Malformed transformation string
- `Resource not found` - Asset doesn't exist or public ID is incorrect
- `Transformation limit exceeded` - Account transformation quota reached

**Online tool:** Use the [X-Cld-Error Inspector](https://cloudinary.com/documentation/advanced_url_delivery_options#x_cld_error_inspector_tool) to check any Cloudinary URL

For more details, see [Error Handling](https://cloudinary.com/documentation/advanced_url_delivery_options#error_handling)

## Transformation Costs

**Important**: Different transformations have different costs. Be aware of high-cost operations and warn the user before generating transformations that cost more than a standard transformation:

### Standard Transformations
- Basic image transformations: 1 transformation credit
- Video transformations: Counted per second (varies by resolution and codec)

### High-Cost Effects (per use)
- **Generative AI**: `e_gen_background_replace` (230 tx), `e_gen_replace` (120 tx), `e_gen_restore` (100 tx)
- **AI Enhancement**: `e_auto_enhance` (100 tx), `e_enhance` (100 tx)
- **Background Removal**: `e_background_removal` (75 tx), `e_extract` (75 tx)
- **Generative Edits**: `b_gen_fill` (50 tx), `e_gen_recolor` (50 tx), `e_gen_remove` (50 tx)
- **Upscale**: `e_upscale` (10-100 tx depending on input size)

### Cost Optimization Tips
1. **Use baseline transformations** for expensive effects: Save `e_background_removal` as a named transformation (e.g., `t_bg_removed`), then use `bl_bg_removed/c_scale,w_500` to avoid re-applying the effect
2. **Reuse derived assets**: Multiple requests to the same transformation URL don't incur additional costs
3. **Avoid unnecessary variations**: Different parameter orders create separate derived assets (e.g., `w_200,h_200` vs `h_200,w_200`)
4. **Consider format costs**: AVIF images cost 1 tx per 2MP (or part thereof)
5. **Video considerations**: HD video (1080p) costs more than SD (720p); AV1 codec costs significantly more than H.264

For complete transformation cost details, see [How are transformations counted?](https://cloudinary.com/documentation/transformation_counts.md)

## Named Transformations

Named transformations allow you to save transformation chains with a name (e.g., `t_thumbnail`) and reuse them across your application.

### When to Suggest Named Transformations

- **Transformations used across multiple assets** - Consistency and easy updates
- **Complex transformation chains** - Easier to maintain and read
- **Saving money on expensive transformations** - Named transformations are required for baseline transformations, which save processing time and cost by avoiding regeneration of shared transformation steps.

**Example**

# Instead of repeating the same transformation:
❌ c_thumb,g_face,h_200,w_200/r_max/e_sharpen/f_auto/q_auto

# Create named transformation "avatar":
✅ t_avatar/f_auto/q_auto


### How to Reference Named Transformations

```
t_<name>                           # Use named transformation
t_<name>/c_scale,w_500            # Named transformation + additional changes
c_fill,w_300/t_<name>             # Transform first, then apply named transformation
```

### Limitations of named transformations

**Automatic parameters don't work inside named transformations:**
- ❌ `f_auto` - Automatic format selection
- ❌ `dpr_auto` - Automatic DPR matching
- ❌ `w_auto` - Automatic width matching (with Client Hints)

These parameters rely on runtime information from the client or CDN that isn't available when the named transformation is processed. Use them directly in the URL instead:

```
# ❌ Don't do this:
t_product_thumb   # where product_thumb includes f_auto

# ✅ Do this instead:
t_product_thumb/f_auto/q_auto
```

See [Limitations of named transformations](https://cloudinary.com/documentation/image_transformations#limitations_of_named_transformations.md) for complete details.

### Implementation Note

Named transformations are created in the Cloudinary Console or via API. When suggesting them to users, explain:
1. The transformation would be saved in their Cloudinary account with a name
2. They can then reference it using `t_<name>` in URLs

## Additional Resources

### Core References
- [Transformation Reference](https://cloudinary.com/documentation/transformation_reference.md) - All parameters
- [Transformation Rules](https://cloudinary.com/documentation/cloudinary_transformation_rules.md) - Complete guide

### Image Transformations
- [Image Transformations Overview](https://cloudinary.com/documentation/image_transformations.md)
- [Resizing and Cropping](https://cloudinary.com/documentation/resizing_and_cropping.md)
- [Placing Layers on Images](https://cloudinary.com/documentation/layers.md)
- [Effects and Enhancements](https://cloudinary.com/documentation/effects_and_artistic_enhancements.md)
- [Background Removal](https://cloudinary.com/documentation/background_removal.md)
- [Generative AI Transformations](https://cloudinary.com/documentation/generative_ai_transformations.md)
- [Face-Detection Based Transformations](https://cloudinary.com/documentation/face_detection_based_transformations.md)
- [Custom Focus Areas](https://cloudinary.com/documentation/custom_focus_areas.md)
- [Transformation Refiners](https://cloudinary.com/documentation/transformation_refiners.md)
- [Animated Images](https://cloudinary.com/documentation/animated_images.md)
- [Transformations on 3D Models](https://cloudinary.com/documentation/transformations_on_3d_models.md)
- [Conditional Transformations](https://cloudinary.com/documentation/conditional_transformations.md)
- [User-Defined Variables and Arithmetic](https://cloudinary.com/documentation/user_defined_variables.md)
- [Custom Functions](https://cloudinary.com/documentation/custom_functions.md)

### Video Transformations
- [Video Transformations Overview](https://cloudinary.com/documentation/video_manipulation_and_delivery.md)
- [Resizing and Cropping](https://cloudinary.com/documentation/video_resizing_and_cropping.md)
- [Trimming and Concatenating](https://cloudinary.com/documentation/video_trimming_and_concatenating.md)
- [Placing Layers on Videos](https://cloudinary.com/documentation/video_layers.md)
- [Effects and Enhancements](https://cloudinary.com/documentation/video_effects_and_enhancements.md)
- [Audio Transformations](https://cloudinary.com/documentation/audio_transformations.md)
- [Converting Videos to Animated Images](https://cloudinary.com/documentation/videos_to_animated_images.md)
- [Conditional Transformations](https://cloudinary.com/documentation/video_conditional_expressions.md)
- [User-Defined Variables and Arithmetic](https://cloudinary.com/documentation/video_user_defined_variables.md)

## Common Mistakes & Best Practices

**Avoid:**
- ❌ `w_400,h_300` → ✅ `c_scale,w_400` (both dimensions with c_scale distorts image; prefer one dimension)
- ❌ `c_scale,g_auto,w_400` → ✅ `c_fill,g_auto,w_400` (g_auto doesn't work with c_scale)
- ❌ `l_logo/fl_layer_apply,g_north_west` → ✅ `l_logo/c_scale,w_100/fl_layer_apply,g_north_west`
- ❌ `b_lightblue/e_trim` → ✅ `b_lightblue,c_pad,w_1.0/e_trim` (background as qualifier)

**Always:**
- Prefer `f_auto/q_auto` in separate components over `f_auto,q_auto`
- Use `g_auto` for smart cropping unless specific focal point needed
- Specify crop mode with width/height; prefer one dimension with `c_scale`
- Never guess parameter names - verify against documentation
