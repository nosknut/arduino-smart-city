import { Canvas } from '@react-three/fiber'
import React from 'react'
import THREE from 'three';

var jsonLoader = new THREE.JSONLoader();
jsonLoader.load("models/object.json", addModelToScene);

function addModelToScene(geometry, materials) {
    var material = new THREE.MeshFaceMaterial(materials);
    var object = new THREE.Mesh(geometry, material);
    object.scale.set(10, 10, 10);
    scene.add(object);
}

export const CityScene = React.memo(() => {

    return (

        <Canvas events={(state => {
            state.getState().scene.
        })}>
            <ambientLight intensity={0.1} />
            <spotLight position={[10, 10, 10]} angle={0.15} penumbra={0.1} />
            <pointLight position={[-10, -10, -10]} />
            <LoadSc
        </Canvas>
    )
})
