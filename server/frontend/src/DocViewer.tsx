import * as React from "react";
import { useLoaderData, Params } from "react-router-dom";
import { TOOL_AUTO } from "react-svg-pan-zoom";
import { MODE_IDLE } from "react-svg-pan-zoom";
import { ReactSVGPanZoom, TOOL_NONE, Value, Tool } from 'react-svg-pan-zoom';

export const loader = async (args: {
    params: Params<string>
}) => {
    const params = args.params as { docId: string };
    return { docId: params.docId };
}
type LoaderReturn = Awaited<ReturnType<typeof loader>>;


export default () => {
    const loaderReturn = useLoaderData() as LoaderReturn;
    const [diagramContents, setDiagramContents] = React.useState<string>("");
    return <>
        <h1>Document {loaderReturn.docId}</h1>
        <textarea value={diagramContents} onChange={(evt) => setDiagramContents(evt.target.value)}></textarea>
        <Diagram diagramContents={diagramContents}></Diagram>
    </>
};

const Diagram = (props: {
    diagramContents: string
}) => {
    const [lastSVG, setLastSVG] = React.useState<string>("");
    React.useEffect(() => {
        setLastSVG(props.diagramContents);
    }, [
        props.diagramContents
    ])

    const Viewer = React.useRef(null);
    const [tool, setTool] = React.useState<Tool>(TOOL_AUTO)
    const [value, setValue] = React.useState<Value>({
        version: 2,
        mode: MODE_IDLE,
        focus: true,
        a: 1,
        b: 1,
        c: 1,
        d: 1,
        e: 1,
        f: 1,
        viewerWidth: 500,
        viewerHeight: 500,
        SVGWidth: 500,
        SVGHeight: 500,
        miniatureOpen: false
    })


    return <ReactSVGPanZoom
        width={900} height={600}
        tool={tool} onChangeTool={setTool}
        value={value} onChangeValue={setValue}
        detectAutoPan={false}
    >
        <div dangerouslySetInnerHTML={{ __html: lastSVG}}>
        </div>
    </ReactSVGPanZoom>
}