from glLibLocals import *
from glLibError import *
def glLibInternal_shader(type,args):
    renderequation = ""
    uservars = ""
    prevertex = ""
    verttrans = ""
    postvertex = ""
    uvtrans = ""
    extfuncvert = ""
    extfuncfrag = ""
    max1Dtextures = 0
    max2Dtextures = 8
    max3Dtextures = 0
    maxcubetextures = 0
    maxrendertargets = 1
    if type == GLLIB_BLANK: #Passed
        renderequation = "color = vec4(1.0);"
        max2Dtextures = 0
    elif type == GLLIB_PHONG: #Passed
        renderequation = "vec3 lvec=light_vector(0);color.rgb=((ambient_color*light_ambient(0))+(((diffuse_color*light_diffuse(0,diffuse_coefficient(normal,lvec)))+(specular_color*light_specular(0,specular_coefficient_ph(normal,lvec))))*light_att(0))).rgb;"
        max2Dtextures = 0
##    elif type == GLLIB_BLINN: #Not Passed
##        renderequation = "vec3 lvec=light_vector(0);color.rgb=((ambient_color*light_ambient(0))+(((diffuse_color*light_diffuse(0,diffuse_coefficient(normal,lvec)))+(specular_color*light_specular(0,specular_coefficient_bl(normal))))*light_att(0))).rgb;"
    elif type == GLLIB_TEXTURE: #Passed
        renderequation = "color = texture2D(tex2D_1,uv);"
        max2Dtextures = 1
    elif type == GLLIB_VIEW_DEPTHBUFFER: #Passed
        renderequation = "color = vec4(1.0-vec3(float(gl_FragCoord.z-gl_DepthRange.near)/float(gl_DepthRange.far-gl_DepthRange.near)),1.0);"
        max2Dtextures = 0
    elif type == GLLIB_VIEW_NORMALS: #Close enough
        renderequation = "color = vec4((n.xy+1.0)/2.0,n.z,1.0);"
        max2Dtextures = 0
    elif type == GLLIB_POSITION_MAP: #Right--I think...
        uservars = "uniform vec2 size;uniform bool stage1;uniform int fbotype;uniform int type;uniform int render_pass;"
        renderequation = """
        if (  (render_pass>1)  &&  (gl_FragCoord.z<=texture2D(tex2D_1,gl_FragCoord.xy*(1.0/size)).r)  ) { discard; }
        else {
            if (fbotype==1) {
                if (stage1) {
                    float depth = (gl_FragCoord.z-gl_DepthRange.near)/float(gl_DepthRange.far-gl_DepthRange.near);
                    if      (type==1) {                color.r = depth; } //receiver
                    else if (type==2) { color.g = 0.5; color.b = depth; } //refractive
                    else if (type==3) { color.g = 1.0; color.b = depth; } //reflective
                }
                else {
                    color.rgb = vec3(normal*0.5)+vec3(0.5);
                }
            }
            else if (fbotype==2) {
                float depth = (gl_FragCoord.z-gl_DepthRange.near)/float(gl_DepthRange.far-gl_DepthRange.near);
                if          (type==1) {                color.r = depth; } //receiver
                else {
                    if      (type==2) { color.g = 0.5; color.b = depth; } //refractive
                    else if (type==3) { color.g = 1.0; color.b = depth; } //reflective
                    color2.rgb = vec3(normal*0.5)+vec3(0.5); //in if because receiver normals are irrelevant
                }
            }
        }"""
        max2Dtextures = 1
        maxrendertargets = 3
    elif type == GLLIB_CAUSTIC_MAP: #reflection backwards needs work!
        uservars = """
        uniform float eta;
        uniform float brightness;
        uniform float grid_sc;
        uniform vec2 size;
        varying float continuing;"""
        extfuncvert = """
        vec2 get_coord(vec2 v, vec2 size) { return vec2(v.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size); }"""
        verttrans = """
        vertex.xy = vec2(grid_sc*(vertex.xy-vec2(0.5)))+vec2(0.5);
        vec2 coord = get_coord(vertex.xy,size);
        vec4 sample = texture2D(tex2D_2,coord);
        
        continuing = 1.0;
        if (sample.g==0.0) { continuing=0.0; }
        else {
            float delta_depth = sample.r-sample.b;
            vertex.xy = (coord*size)+vec2(0.5);
            vec3 normal = normalize(texture2D(tex2D_3,coord).rgb-vec3(0.5));
            normal.z = -normal.z;
            vec3 lightdir = vec3(0.0,0.0,1.0);//normalize(vec3(vec2(0.5)-coord,sample.b));
            if (abs(sample.g-0.5)<0.05) {
                if (delta_depth<0.0) { continuing = 0.0; }
                else {
                    float refract_eta = eta;
                    if (dot(lightdir,normal)>0.0) { refract_eta = 1.0/refract_eta; normal *= -1.0; }
                    vec3 refractedray = refract(lightdir,normal,refract_eta);
                    vertex.xy += size*(delta_depth/refractedray.z)*refractedray.xy;
                }
            }
            else if (delta_depth>0.0) {
                vec3 reflectedray = reflect(lightdir,normal);
                vertex.xy += size*(abs(delta_depth)/reflectedray.z)*reflectedray.xy;
                //coord = get_coord(vertex.xy,size);
                //sample = texture2D(tex2D_1,coord);
                //delta_depth = sample.r-sample.b;
                if (reflectedray.z<0.0) { //reflecting back
                    if (delta_depth>0.0) { continuing = 0.0; }
                    else                 { continuing = 1.0; }
                }
                else { //reflecting away
                    if (delta_depth<0.0) { continuing = 0.0; }
                    else                 { continuing = 1.0; }
                }
                
            }
            else { continuing = 0.0; }
        }"""
        renderequation = """
        if (continuing==0.0) { discard; }
        vec2 v_rot = normalize(vertex.zw);
        vec4 l_uv = vec4(0.0,0.0,gl_PointCoord.xy);
        l_uv.zw-=vec2(0.5,0.5);l_uv.x=l_uv.z*v_rot.x;l_uv.y=l_uv.w*v_rot.x;l_uv.x-=l_uv.w*v_rot.y;l_uv.y+=l_uv.z*v_rot.y;
        color = texture2D(tex2D_1,l_uv.xy+vec2(0.5,0.5));
        color.rgb *= brightness;"""
        max2Dtextures = 3
    elif type == GLLIB_DEPTH_PEEL:
        uservars = "uniform vec2 size;uniform bool stage1;uniform float near;uniform float far;"
        renderequation = """
        color.rgb = vec3(1.0);
        if (!stage1) { if (gl_FragCoord.z<=texture2D(tex2D_1,gl_FragCoord.xy*(1.0/size)).r) { discard; } }"""
        max2Dtextures = 1
        maxrendertargets = 1
##    elif type == GLLIB_DEPTH_PEEL_SINGLE_PASS:
##        uservars = "uniform vec2 size;"
##        extfuncfrag = """
##        void move_2_to_1(float depth) {                               gl_FragData[0].r=depth;gl_FragDepth=depth; }
##        void move_3_to_2(float depth) { move_2_to_1(gl_FragData[1].r);gl_FragData[1].r=depth;gl_FragDepth=depth; }
##        void move_4_to_3(float depth) { move_3_to_2(gl_FragData[2].r);gl_FragData[2].r=depth;gl_FragDepth=depth; }
##        void move_5_to_4(float depth) { move_4_to_3(gl_FragData[3].r);gl_FragData[3].r=depth;gl_FragDepth=depth; }
##        void move_6_to_5(float depth) { move_5_to_4(gl_FragData[4].r);gl_FragData[4].r=depth;gl_FragDepth=depth; }
##        void move_7_to_6(float depth) { move_6_to_5(gl_FragData[5].r);gl_FragData[5].r=depth;gl_FragDepth=depth; }
##        void move_8_to_7(float depth) { move_7_to_6(gl_FragData[6].r);gl_FragData[6].r=depth;gl_FragDepth=depth; }
##        void move_9_to_8(float depth) { move_8_to_7(gl_FragData[7].r);gl_FragData[7].r=depth;gl_FragDepth=depth; }"""
##        renderequation = """
##        float depth = gl_FragCoord.z;
##        float d1 = gl_FragData[0].r;
##        float d2 = gl_FragData[1].r;
##        float d3 = gl_FragData[2].r;
##        float d4 = gl_FragData[3].r;
##        float d5 = gl_FragData[4].r;
##        float d6 = gl_FragData[5].r;
##        float d7 = gl_FragData[6].r;
##        float d8 = gl_FragData[7].r;
##        if      (depth>d8) { discard; }
##        else if (depth>d7) { move_2_to_1(gl_FragCoord.z); }
##        else if (depth>d6) { move_3_to_2(gl_FragCoord.z); }
##        else if (depth>d5) { move_4_to_3(gl_FragCoord.z); }
##        else if (depth>d4) { move_5_to_4(gl_FragCoord.z); }
##        else if (depth>d3) { move_6_to_5(gl_FragCoord.z); }
##        else if (depth>d2) { move_7_to_6(gl_FragCoord.z); }
##        else if (depth>d1) { move_8_to_7(gl_FragCoord.z); }
##        else               { move_9_to_8(gl_FragCoord.z); }"""
##        max2Dtextures = 0
##        maxrendertargets = 8
    elif type == GLLIB_PARTICLE_UPDATE:
        uservars = """
        uniform float size;
        uniform float step;
        uniform vec3 scale;
        uniform vec3 forces;
        uniform vec3 jitter;
        uniform vec3 initialspeed;
        uniform vec3 initalpos;
        uniform vec2 xedge;
        uniform vec2 yedge;
        uniform vec2 zedge;
        varying vec2 coord;"""
        verttrans = """
        coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        vec4 pos_time = texture2D(tex2D_1,coord);
        
        vec4 velocity_sample = texture2D(tex2D_2,coord);
        vec3 direction = vec3(velocity_sample.xyz-vec3(0.5))*2.0;
        float speed = velocity_sample.w;
        vec3 velocity = speed*direction;
        
        pos_time.w += step;
        
        if(pos_time.w>=1.0){
            velocity = initialspeed + vec3(jitter*vec3(texture2D(tex2D_3,coord).xyz-vec3(0.5)));
            pos_time.xyz = initalpos + vec3(0.5);
            pos_time.w = 0.0;
        }
        
        velocity += forces;
        
        pos_time.xyz += velocity;
        if      (pos_time.x<0.0) { pos_time.x=0.0;velocity.x*=xedge.x; }
        else if (pos_time.x>1.0) { pos_time.x=1.0;velocity.x*=xedge.y; }
        if      (pos_time.y<0.0) { pos_time.y=0.0;velocity.y*=yedge.x; }
        else if (pos_time.y>1.0) { pos_time.y=1.0;velocity.y*=yedge.y; }
        if      (pos_time.z<0.0) { pos_time.z=0.0;velocity.z*=xedge.x; }
        else if (pos_time.z>1.0) { pos_time.z=1.0;velocity.z*=xedge.y; }
        color = pos_time;
        float new_speed = length(velocity);
        color2 = vec4(vec3(normalize(velocity.xyz)*0.5)+vec3(0.5),new_speed);"""
        max2Dtextures = 4
        maxrendertargets = 2
    elif type == GLLIB_PARTICLE_DRAW:
        uservars = """uniform float size;
        uniform float fade;
        uniform vec3 trans;
        uniform vec3 scale;
        uniform float point_size;
        varying float continuing;
        varying float intensity;"""
        verttrans = """
        vec2 coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec4 pos_time = texture2D(tex2D_1,coord);
        intensity = 1.0 - pow(pos_time.w,fade);
        vertex.xyz = pos_time.xyz - vec3(0.5);
        vertex = vec4(vec3(vertex.xyz*scale*2.0)+trans,1.0);"""
        postvertex = """
        continuing = 0.0;
        gl_PointSize = point_size/length(gl_Position);
        continuing = clamp(floor(gl_PointSize),0.0,1.0);"""
        renderequation = """
        vec2 v_rot = normalize(vertex.zw);
        vec4 l_uv = vec4(0.0,0.0,gl_PointCoord.xy);
        l_uv.zw-=vec2(0.5,0.5);l_uv.x=l_uv.z*v_rot.x;l_uv.y=l_uv.w*v_rot.x;l_uv.x-=l_uv.w*v_rot.y;l_uv.y+=l_uv.z*v_rot.y;
        color = texture2D(tex2D_2,l_uv.xy+vec2(0.5,0.5));
        color.a *= intensity*continuing;"""
        max2Dtextures = 2
    elif type == GLLIB_CLOTH_DISTANCE:
        #doesn't need to take into account scale, trans, and is in the range [0,1]
        #instead of [-1,1] in 3D, b/c the corresponding update and normal shaders don't either.
        uservars = """
        uniform vec2 size;
        uniform float stretched;
        uniform bool repeat_x;
        uniform bool repeat_y;
        varying vec4 kernel_edges;
        varying vec4 kernel_corners;"""
        verttrans = """
        vec2 vert_uv; vec2 delta; vec2 delta_coord; float distance; vec3 vert;
        vert_uv = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec3 center = texture2D(tex2D_1,vert_uv).rgb;

        for (int x_uv=-1; x_uv<1+1; x_uv++) { for (int y_uv=-1; y_uv<1+1; y_uv++) {
            if (!((x_uv==0)&&(y_uv==0))) {
                delta = vec2(float(x_uv),float(y_uv));
                delta_coord = delta/vec2(size);
                vert_uv = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size)+delta_coord;
                
                vert = texture2D(tex2D_1,vert_uv).rgb;
                distance = length(center-vert);
                distance *= stretched;
                if      (y_uv==-1) { if      (x_uv==-1) { kernel_corners.x = distance; }
                                     else if (x_uv== 0) { kernel_edges.x   = distance; }
                                     else if (x_uv== 1) { kernel_corners.y = distance; } }
                else if (y_uv== 0) { if      (x_uv==-1) { kernel_edges.y   = distance; }
                                     else if (x_uv== 1) { kernel_edges.z   = distance; } }
                else if (y_uv== 1) { if      (x_uv==-1) { kernel_corners.z = distance; }
                                     else if (x_uv== 0) { kernel_edges.w   = distance; }
                                     else if (x_uv== 1) { kernel_corners.w = distance; } }
            }
        }}
        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color  = kernel_edges;
        color2 = kernel_corners;"""
        max2Dtextures = 2
        maxrendertargets = 2
    elif type == GLLIB_CLOTH_UPDATE:
        uservars = """
        uniform vec2 size;
        uniform vec3 gravity;
        uniform float dampening;
        uniform float max_jitter;
        uniform float tensor;
        uniform float angle_tensor;
        uniform float time_step;
        uniform int kernel_size;
        uniform bool repeat_x;
        uniform bool repeat_y;
        
        varying vec3 position;
        varying vec3 velocity;
        varying float restrained;
        varying vec3 vec;"""
        verttrans = """
        vec2 coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec4 position_restrained = texture2D(tex2D_1,coord);
        velocity                 = 2.0*vec3(texture2D(tex2D_2,coord).rgb-vec3(0.5));
        vec3 inter_cloth_forces  = vec3(0.0);
        vec4 kernel_edges        = texture2D(tex2D_3,coord);
        vec4 kernel_corners      = texture2D(tex2D_4,coord);
        position = position_restrained.rgb; //in range [0,1]; not [-1,1]
        restrained = position_restrained.a;
        
        if (restrained==0.0) {
            vec2 delta; vec2 delta_coord;
            vec3 spring_vec; vec3 norm_spring_vec; vec3 force_vec;
            float vec_length; float target_length=0.0; float force_scalar; bool continuing;
            vec3 left_edge = vec3(0.0);
            vec3 right_edge = vec3(0.0);
            vec3 top_edge = vec3(0.0);
            vec3 bottom_edge = vec3(0.0);
            for (int x_uv=-kernel_size; x_uv<kernel_size+1; x_uv++) { for (int y_uv=-kernel_size; y_uv<kernel_size+1; y_uv++) {
                if (!((x_uv==0)&&(y_uv==0))) {
                    delta = vec2(float(x_uv),float(y_uv));
                    delta_coord = delta/vec2(size);
                    coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size)+delta_coord;
                    continuing = true;
                    if (!((coord.x>0.0)&&(coord.x<1.0))) {
                        if (repeat_x) { coord.x = mod(coord.x,1.0); }
                        else { continuing = false; }
                    }
                    if (!((coord.y>0.0)&&(coord.y<1.0))) {
                        if (repeat_y) { coord.y = mod(coord.y,1.0); }
                        else { continuing = false; }
                    }
                    if (continuing) {
                        spring_vec = position - texture2D(tex2D_1,coord).rgb;
                        vec_length = length(spring_vec);
                        norm_spring_vec = spring_vec / vec_length;
                        if      (y_uv==-1) { if      (x_uv==-1) { target_length = kernel_corners.x;                                }
                                             else if (x_uv== 0) { target_length = kernel_edges.x  ; bottom_edge = norm_spring_vec; }
                                             else if (x_uv== 1) { target_length = kernel_corners.y;                                } }
                        else if (y_uv== 0) { if      (x_uv==-1) { target_length = kernel_edges.y  ;   left_edge = norm_spring_vec; }
                                             else if (x_uv== 1) { target_length = kernel_edges.z  ;  right_edge = norm_spring_vec; } }
                        else if (y_uv== 1) { if      (x_uv==-1) { target_length = kernel_corners.z;                                }
                                             else if (x_uv== 0) { target_length = kernel_edges.w  ;    top_edge = norm_spring_vec; }
                                             else if (x_uv== 1) { target_length = kernel_corners.w;                                } }
                        //distance correction
                        if (target_length!=0.0) {
                            force_scalar = (vec_length-target_length)/target_length;
                            force_vec = force_scalar*-norm_spring_vec;
                            inter_cloth_forces += force_vec;
                        }
                    }
                }
            }}
            inter_cloth_forces *= tensor;
            
            //angle correction
            float trig; vec3 bisect_vec;
            float cos_angle = dot(left_edge,right_edge);
            if ((cos_angle>0.0)&&(cos_angle<1.0)) {
                trig = acos(cos_angle)/3.1416;
                vec = left_edge + right_edge;
                vec_length = length(vec);
                if ((vec_length<=2.0)&&(vec_length!=0.0)) {
                    bisect_vec = vec/vec_length;
                    inter_cloth_forces += bisect_vec*(1.0-pow(trig,16.0))*angle_tensor;
                }
            }
            
            float jitter_length = length(inter_cloth_forces);
            if (jitter_length>max_jitter) { inter_cloth_forces *= 0.5; }
            
            velocity += vec3(inter_cloth_forces);
            velocity *= dampening;
            velocity += gravity;
            position += time_step*velocity;
        }
        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color.rgb  = position;
        color.a = restrained;
        color2.rgb = vec3(velocity*0.5)+vec3(0.5);
        color3.rgb = vec3(vec*0.5)+vec3(0.5);"""
        max2Dtextures = 4
        maxrendertargets = 3
    elif type == GLLIB_CLOTH_COLLIDE:
        uservars = """
        uniform int num_obstacles;
        uniform vec2 size;
        uniform vec3 voxel_size; //size per side 2D, size per side 3D, and tiles per side
        uniform bool is_garment;
        varying vec3 position;
        varying vec3 velocity;
        varying float restrained;
        const float two_pi = 6.283185;
        varying vec3 send;"""
        extfuncvert = """
        bool voxel_sample_sum_is_zero(vec2 coord) {
            return sum(texture2D(tex2D_4,coord))==0.0;
        }"""
        verttrans = """
        vec2 coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec4 position_restrained = texture2D(tex2D_1,coord);
        velocity                 = 2.0*vec3(texture2D(tex2D_2,coord).rgb-vec3(0.5));
        vec3 vec                 = 2.0*vec3(texture2D(tex2D_3,coord).rgb-vec3(0.5));
        position = position_restrained.rgb; //in range [0,1]; not [-1,1]
        restrained = position_restrained.a;
        if (restrained==0.0) {
            if (is_garment) {
                //vec3 collide_position = floor(position*voxel_size.y);
                vec3 collide_position = position*2.0;
                if ((collide_position.x>0.5)&&(collide_position.x<1.5)&&
                    (collide_position.y>0.5)&&(collide_position.y<1.5)&&
                    (collide_position.z>0.5)&&(collide_position.z<1.5)) {
                    collide_position -= vec3(0.5);
                    vec3 collide_position_voxel = floor(collide_position*voxel_size.y);
                    coord = vec2(0.5) + collide_position_voxel.xz;
                    coord += voxel_size.y*vec2(mod(collide_position_voxel.y,voxel_size.z),floor(collide_position_voxel.y/voxel_size.z));
                    coord /= voxel_size.x;
                    vec3 obstacle_pos = texture2D(tex2D_4,coord).xyz;
                    send = vec3(coord.xy,0.0);
                    if (obstacle_pos.x==1.0) {
                    //restrained = 1.0;
                        /*collide_position *= voxel_size.y;
                        vec3 transformed_position = collide_position-round(collide_position);
                        vec3 abs_delta_vec = abs(transformed_position);
                        vec3 sign_delta_vec = sign(transformed_position);
                        abs_delta_vec *= 1.0/voxel_size.y;
                        float maximum = min(abs_delta_vec.x,min(abs_delta_vec.y,abs_delta_vec.z));
                        vec3 add_vec = vec3(0.0);
                        float one_pix = 1.0/voxel_size.x;
                        bool voxel_filled;
                        if (maximum==abs_delta_vec.x) {
                            voxel_filled = false;//voxel_sample_sum_is_zero(coord+vec2(one_pix*sign_delta_vec.x,0.0));
                            if (voxel_filled) {
                                maximum=max(abs_delta_vec.y,abs_delta_vec.z);
                                if (maximum==abs_delta_vec.y) {
                                    voxel_filled = voxel_sample_sum_is_zero(coord+vec2(0.0,one_pix*sign_delta_vec.y));
                                    if (voxel_filled) { maximum=abs_delta_vec.z; }
                                    else { add_vec = vec3(0.0,maximum*sign_delta_vec.y,0.0); }
                                }
                                if (maximum==abs_delta_vec.z) {
                                    add_vec = vec3(0.0,0.0,maximum*sign_delta_vec.z);
                                }
                            }
                            else { add_vec = vec3(abs_delta_vec.x*sign_delta_vec.x,0.0,0.0); }
                        }
                        if (maximum==abs_delta_vec.y) {
                            voxel_filled = false;//voxel_sample_sum_is_zero(coord+vec2(0.0,one_pix*-sign_delta_vec.y));
                            if (voxel_filled) { maximum=abs_delta_vec.z; }
                            else { add_vec = vec3(0.0,abs_delta_vec.y*-sign_delta_vec.y,0.0); }
                        }
                        if (maximum==abs_delta_vec.z) {
                            add_vec = vec3(0.0,0.0,abs_delta_vec.z*sign_delta_vec.z);
                        }
                        //add_vec = vec3(0.0,abs_delta_vec.y*-sign_delta_vec.y,0.0);
                        //add_vec /= voxel_size.y;
                        
                        position += add_vec;
                        //velocity *= 0.9;
                        */
                    }
                }
            }
            else {
                vec4 obstacle_param1;vec4 obstacle_param2;vec3 obstacle_pos;
                float radius; float f_num_obstacles = float(num_obstacles);
                
                float xangle; float yangle; float cos_xangle; float sin_xangle; float cos_yangle; float sin_yangle; float maximum;
                vec3 transformed_position; vec3 abs_delta_vec; vec3 add_vec; mat3 rot_x; mat3 rot_y;
                for (int obstacle=0;obstacle<num_obstacles;obstacle++) {
                    coord = vec2( ((float(obstacle)/(f_num_obstacles-1.0))*(1.0-(1.0/f_num_obstacles)))+(0.5/f_num_obstacles), 0.5 );
                    obstacle_param1 = texture2D(tex2D_4,coord);
                    obstacle_pos = 2.0*obstacle_param1.xyz;
                    if (obstacle_pos.z>=1.0) {
                        obstacle_pos.z -= 1.0;
                        vec = position - obstacle_pos;
                        radius = obstacle_param1.a;
                        if (length(vec)<radius) {
                            vec3 vec_normalized = normalize(vec);
                            position = vec_normalized*radius+obstacle_pos;
                            velocity *= 0.9;
                    }}
                    else if (obstacle_pos.y>=1.0) {
                        obstacle_pos.y -= 1.0;
                        obstacle_param2 = texture2D(tex2D_5,coord);
                        xangle = obstacle_param2.z*two_pi;
                        yangle = obstacle_param2.w*two_pi;
                        cos_xangle=cos(-xangle);sin_xangle=sin(-xangle);cos_yangle=cos(-yangle);sin_yangle=sin(-yangle);
                        rot_x = mat3(vec3(        1.0, 0.0,        0.0       ),
                                     vec3(        0.0, cos_yangle,-sin_yangle),
                                     vec3(        0.0, sin_yangle, cos_yangle));
                        rot_y = mat3(vec3( cos_xangle,        0.0, sin_xangle),
                                     vec3(        0.0,        1.0, 0.0       ),
                                     vec3(-sin_xangle,        0.0, cos_xangle));
                        transformed_position = rot_x*rot_y*(position-obstacle_pos.xyz);
                        if (((transformed_position.x>-obstacle_param1.w)&&(transformed_position.x<obstacle_param1.w))&&
                            ((transformed_position.y>-obstacle_param2.x)&&(transformed_position.y<obstacle_param2.x))&&
                            ((transformed_position.z>-obstacle_param2.y)&&(transformed_position.z<obstacle_param2.y))) {
                            abs_delta_vec = abs(transformed_position);
                            maximum = max(abs_delta_vec.x,max(abs_delta_vec.y,abs_delta_vec.z));
                            add_vec = vec3(0.0);
                            if      (maximum==abs_delta_vec.x) { add_vec = vec3((obstacle_param1.w-maximum)*sign(transformed_position.x),0.0,0.0); }
                            else if (maximum==abs_delta_vec.y) { add_vec = vec3(0.0,(obstacle_param2.x-maximum)*sign(transformed_position.y),0.0); }
                            else                               { add_vec = vec3(0.0,0.0,(obstacle_param2.y-maximum)*sign(transformed_position.z)); }
                            
                            cos_xangle=cos(xangle);sin_xangle=sin(xangle);cos_yangle=cos(yangle);sin_yangle=sin(yangle);
                            mat3 rot_x = mat3(vec3(        1.0, 0.0,        0.0       ),
                                              vec3(        0.0, cos_yangle,-sin_yangle),
                                              vec3(        0.0, sin_yangle, cos_yangle));
                            mat3 rot_y = mat3(vec3( cos_xangle,        0.0, sin_xangle),
                                              vec3(        0.0,        1.0, 0.0       ),
                                              vec3(-sin_xangle,        0.0, cos_xangle));
                            add_vec = rot_x*rot_y*add_vec;
                            
                            position += add_vec;
                            velocity *= 0.9;
                    }}
            }}
        }
        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color.rgb  = position;
        color.a = restrained;
        color2.rgb = vec3(velocity*0.5)+vec3(0.5);
        color3.rgb = send;"""
        max2Dtextures = 5
        maxrendertargets = 3
    elif type == GLLIB_CLOTH_NORMAL:
        uservars = """
        uniform vec2 size;
        uniform bool repeat_x;
        uniform bool repeat_y;
        uniform bool normal_flip;"""
        verttrans = """
        vec2 vert_uv = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec3 center = texture2D(tex2D_1,vert_uv).rgb;
        
        vec2 temp_vert_uv=vec2(0.0);
        vec3 temp_vert;
        vec3 diff_vec1=vec3(0.0);vec3 diff_vec2=vec3(0.0);vec3 diff_vec3=vec3(0.0);vec3 diff_vec4=vec3(0.0);

        float invert = -1.0;
        
        temp_vert_uv = vert_uv + (vec2(1.0,0.0)/size);
        if ((temp_vert_uv.x>1.0)&&(!repeat_x)) { diff_vec1 = vec3(0.0); }
        else {
            temp_vert = texture2D(tex2D_1,temp_vert_uv).rgb;
            diff_vec1 = normalize(temp_vert-center);
        }
        
        temp_vert_uv = vert_uv + (vec2(-1.0,0.0)/size);
        if ((temp_vert_uv.x<0.0)&&(!repeat_x)) { diff_vec2 = vec3(0.0); }
        else {
            temp_vert = texture2D(tex2D_1,temp_vert_uv).rgb;
            diff_vec2 = normalize(temp_vert-center);
        }
            
        temp_vert_uv = vert_uv + (vec2(0.0,1.0)/size);
        if ((temp_vert_uv.y>1.0)&&(!repeat_y)) { diff_vec3 = vec3(0.0); }
        else {
            temp_vert = texture2D(tex2D_1,temp_vert_uv).rgb;
            diff_vec3 = normalize(temp_vert-center);
        }

        temp_vert_uv = vert_uv + (vec2(0.0,-1.0)/size);
        if ((temp_vert_uv.y<0.0)&&(!repeat_y)) { diff_vec4 = vec3(0.0); }
        else {
            temp_vert = texture2D(tex2D_1,temp_vert_uv).rgb;
            diff_vec4 = normalize(temp_vert-center);
        }
        
        vec3 x_vec = diff_vec1 - diff_vec2;
        vec3 y_vec = diff_vec3 - diff_vec4;

        realnorm = invert*normalize(cross(y_vec,x_vec));
        if (normal_flip) { realnorm *= -1.0; }

        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color.rgb = (0.5*realnorm)+vec3(0.5);"""
    elif type == GLLIB_CLOTH_DRAW:
        uservars = """
        uniform vec2 size;
        uniform float scale;
        uniform vec3 trans;
        uniform vec2 uv_repeat;
        uniform bool has_texture;
        uniform int numlights;
        varying vec2 cloth_uv;"""
        prevertex = """
        cloth_uv = vertex.xy;
        vec2 coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        realnorm = 2.0*(texture2D(tex2D_3,coord).rgb-vec3(0.5));"""
        verttrans = """
        vertex.xyz = texture2D(tex2D_1,coord).rgb-vec3(0.5);
        vertex = vec4(vec3(vertex.xyz*scale)+trans,1.0);""" #scale is 2.0*the scale.
        renderequation = """
        normal = normalize(normal);
        
        vec3 ambient_light = vec3(0.0,0.0,0.0);
        vec3 diffuse_light = vec3(0.0,0.0,0.0);
        vec3 specular_light = vec3(0.0,0.0,0.0);
        float attenuation = 0.0;
        
        attenuation = light_att(light1);
        ambient_light  += light_ambient(light1).rgb;
        diffuse_light  += light_diffuse(light1).rgb*attenuation;
        specular_light += light_specular_ph(light1).rgb*attenuation;
        if (numlights>1) {
            attenuation = light_att(light2);
            ambient_light  += light_ambient(light2).rgb;
            diffuse_light  += light_diffuse(light2).rgb*attenuation;
            specular_light += light_specular_ph(light2).rgb*attenuation;
            if (numlights>2) {
                attenuation = light_att(light3);
                ambient_light  += light_ambient(light3).rgb;
                diffuse_light  += light_diffuse(light3).rgb*attenuation;
                specular_light += light_specular_ph(light3).rgb*attenuation;
                if (numlights>3) {
                    attenuation = light_att(light4);
                    ambient_light  += light_ambient(light4).rgb;
                    diffuse_light  += light_diffuse(light4).rgb*attenuation;
                    specular_light += light_specular_ph(light4).rgb*attenuation;
                    if (numlights>4) {
                        attenuation = light_att(light5);
                        ambient_light  += light_ambient(light5).rgb;
                        diffuse_light  += light_diffuse(light5).rgb*attenuation;
                        specular_light += light_specular_ph(light5).rgb*attenuation;
                        if (numlights>5) {
                            attenuation = light_att(light6);
                            ambient_light  += light_ambient(light6).rgb;
                            diffuse_light  += light_diffuse(light6).rgb*attenuation;
                            specular_light += light_specular_ph(light6).rgb*attenuation;
                            if (numlights>6) {
                                attenuation = light_att(light7);
                                ambient_light  += light_ambient(light7).rgb;
                                diffuse_light  += light_diffuse(light7).rgb*attenuation;
                                specular_light += light_specular_ph(light7).rgb*attenuation;
                                if (numlights>7) {
                                    attenuation = light_att(light8);
                                    ambient_light  += light_ambient(light8).rgb;
                                    diffuse_light  += light_diffuse(light8).rgb*attenuation;
                                    specular_light += light_specular_ph(light8).rgb*attenuation;
        }}}}}}}
            
        color.rgb += ambient_color.rgb*ambient_light;
        color.rgb += diffuse_color.rgb*diffuse_light;
        color.rgb += specular_color.rgb*specular_light;
        if (has_texture) { color *= texture2D(tex2D_2,cloth_uv*uv_repeat); }"""
        max2Dtextures = 3
    elif type == GLLIB_HAIR_GROW:
        uservars = """
        uniform vec2 size;
        uniform float length_scalar;
        varying vec2 coord;"""
        verttrans = """
        coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color.rgb = texture2D(tex2D_1,coord).xyz;
        color.rgb += length_scalar*texture2D(tex2D_2,coord).xyz;"""
        max2Dtextures = 2
    elif type == GLLIB_HAIR_UPDATE:
        uservars = """
        uniform vec2 size;
        uniform vec3 gravity;
        uniform float dampening;
        uniform float tensor;
        uniform bool end;
        uniform float target_length;
        uniform float time_step;
        
        varying vec3 position;
        varying vec3 velocity;
        varying float current_length;"""
        verttrans = """
        vec2 coord = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        vec3 last_position   = texture2D(tex2D_1,coord).xyz;
        vec4 position_length = texture2D(tex2D_2,coord);
        vec3 next_position   = texture2D(tex2D_3,coord).xyz;
        velocity             = 2.0*vec3(texture2D(tex2D_4,coord).rgb-vec3(0.5));
        position = position_length.rgb; //in range [0,1]; not [-1,1]
        current_length = position_length.a;

        vec3 inter_hair_forces = vec3(0.0);
        
        vec3 spring_vec = position - last_position;
        float vec_length = length(spring_vec);
        //distance correction
        float force_scalar = (vec_length-target_length)/target_length;
        inter_hair_forces += force_scalar*(spring_vec/-vec_length);

        /*
        if (!end) {
            spring_vec = position - next_position;
            vec_length = length(spring_vec);
            //distance correction
            force_scalar = (vec_length-target_length)/target_length;
            inter_hair_forces += force_scalar*(spring_vec/-vec_length);
        }
        */
        
        inter_hair_forces *= tensor;
        velocity += vec3(inter_hair_forces);
        velocity *= dampening;
        velocity += gravity;
        position += time_step*velocity;

        vertex.xy = vec2(vertex.xy*(size-1.0))+vec2(0.5);"""
        renderequation = """
        color.rgb  = position;
        color.a = current_length;
        color2.rgb = vec3(velocity*0.5)+vec3(0.5);"""
        max2Dtextures = 4
        maxrendertargets = 2
    elif type == GLLIB_HAIR_DRAW:
        uservars = """
        uniform vec2 size;
        uniform float scale;
        uniform vec3 trans;
        uniform int hair_length;
        uniform vec3 camerapos;
        uniform float hair_size;
        attribute float quad_side;"""
        prevertex = """
        vec2 coord2D = vec2(vertex.xy*vec2(1.0-(1.0/size)))+vec2(0.5/size);
        //realnorm = 2.0*(texture2D(tex2D_3,coord2D).rgb-vec3(0.5));"""
        verttrans = """
        vec4 sample=vec4(0.0);
        float texture = floor(float(hair_length-1)*vertex.z)+1.0;
        if      (abs(texture-1.0)<0.01) { sample = texture2D(tex2D_1,coord2D); }
        else if (abs(texture-2.0)<0.01) { sample = texture2D(tex2D_2,coord2D); }
        else if (abs(texture-3.0)<0.01) { sample = texture2D(tex2D_3,coord2D); }
        else if (abs(texture-4.0)<0.01) { sample = texture2D(tex2D_4,coord2D); }
        else if (abs(texture-5.0)<0.01) { sample = texture2D(tex2D_5,coord2D); }
        else if (abs(texture-6.0)<0.01) { sample = texture2D(tex2D_6,coord2D); }
        else if (abs(texture-7.0)<0.01) { sample = texture2D(tex2D_7,coord2D); }
        else if (abs(texture-8.0)<0.01) { sample = texture2D(tex2D_8,coord2D); }
        vertex.xyz = sample.rgb-vec3(0.5);
        vec2 camera_vec = normalize(vec3(camerapos-vertex.xyz).xz);
        if (quad_side==1.0) {
            vertex.x -= hair_size*camera_vec.y;
            vertex.z += hair_size*camera_vec.x;
        }
        else {
            vertex.x += hair_size*camera_vec.y;
            vertex.z -= hair_size*camera_vec.x;
        }
        vertex = vec4(vec3(vertex.xyz*scale)+trans,1.0);"""
        renderequation = """
        //normal = normalize(normal);
        //color.rgb += ambient_color.rgb*light_ambient(light1).rgb;
        //color.rgb += diffuse_color.rgb*light_diffuse(light1).rgb;
        //color.rgb += specular_color.rgb*light_specular_ph(light1).rgb;
        color.rgb = vec3(1.0);"""
        max2Dtextures = 16
    elif type == GLLIB_FLUID2D_DIFFUSE:
        uservars = "uniform vec2 size;"
        extfuncfrag = """
        def lin_solve(N, b, x, x0, a, c):
            for k in range(0,20):
                numerator = x0[1:N+1,1:N+1] +
                            a*(x[0:N,1:N+1]+x[2:N+2,1:N+1]+x[1:N+1,0:N]+x[1:N+1,2:N+2])
                x[1:N+1,1:N+1] = numerator/c
            set_bnd(N, b, x)
        vec3 add_source(float dt) {
            return dt*2.0*(texture2D(tex2,gl_FragCoord.xy/size).rg-vec2(0.5));
        }
        diffuse(vec2 size, float b, float diff, float dt) {
            float a = dt*diff*size.x*size.y;
            lin_solve(N,b,x,x0,a,1.0+4.0*a)
        }"""
        renderequation = """
        diffuse(N, 0, x, x0, diff, dt);
        //color = vec4(1.0);"""
        max2Dtextures = 1
    elif type == GLLIB_FLUID2D_ADVECT:
        extfuncfrag = """
        def advect (N, b, d, d0, u, v, dt):
            dt0 = dt*N;
            for i in range(1, N+1):
                for j in range(1, N+1):
                    x = i-dt0*u[i,j]; y = j-dt0*v[i,j]
                    vec2 xy = gl_FragCoord.xy-dt0*texture2D(tex2,);
                    if x<0.5: x=0.5
                    if x>N+0.5: x=N+0.5
                    i0 = floor(x); i1 = i0+1
                    if y<0.5: y=0.5
                    if y>N+0.5: y=N+0.5
                    j0 = floor(y); j1 = j0+1
                    s1 = x-i0; s0 = 1-s1; t1 = y-j0; t0 = 1-t1
                    d[i,j] = s0*(t0*texture2D(tex1,[i0,j0])+t1*d0[i0,j1])+
                             s1*(t0*d0[i1,j0]+t1*d0[i1,j1]);
            set_bnd (N, b, d)"""
        renderequation = """
        advect(N, 0, x, x0, v, dt);"""
        max2Dtextures = 2
    else:
        raise glLibError('Shader type "'+str(type)+'" not found!')
    return renderequation,uservars,prevertex,verttrans,postvertex,uvtrans,extfuncvert,extfuncfrag,max1Dtextures,max2Dtextures,max3Dtextures,maxcubetextures,maxrendertargets
