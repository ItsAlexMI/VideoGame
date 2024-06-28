#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

struct Flashlight {
    vec3 position;
    vec3 direction;
    vec3 color;
    float cutoff;
};

uniform Light light;
uniform Flashlight flashlight;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;

float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}

float getSoftShadowX16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}

vec3 calculateLight(vec3 color, vec3 lightDir, vec3 lightColor, float intensity) {
    vec3 Normal = normalize(normal);

    // Ambient light
    vec3 ambient = light.Ia;

    // Diffuse light
    float diff = max(dot(lightDir, Normal), 0.0);
    vec3 diffuse = diff * light.Id;

    // Specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = spec * light.Is;

    // Shadow calculation
    float shadow = getSoftShadowX16();  // Soft shadow

    return color * (ambient + (diffuse + specular) * shadow);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    // Calculate directional light (main light)
    vec3 lightDir = normalize(light.position - fragPos);
    vec3 result = calculateLight(color, lightDir, light.Id, 1.0);

    // Calculate flashlight
    vec3 flashlightDir = normalize(flashlight.position - fragPos);
    float theta = dot(flashlightDir, normalize(-flashlight.direction));
    if (theta > flashlight.cutoff) {
        float epsilon = flashlight.cutoff - cos(radians(10.0));  // Smooth edge
        float intensity = clamp((theta - flashlight.cutoff) / epsilon, 0.0, 1.0);
        result += calculateLight(color, flashlightDir, flashlight.color, intensity);
    }

    color = pow(result, 1.0 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}
