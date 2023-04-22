import * as React from "react";
import { useLoaderData, Params } from "react-router-dom";
import { TOOL_AUTO } from "react-svg-pan-zoom";
import { MODE_IDLE } from "react-svg-pan-zoom";
import { ReactSVGPanZoom, Value, Tool } from 'react-svg-pan-zoom';
import { ReactSvgPanZoomLoader } from 'react-svg-pan-zoom-loader';
export const loader = async (args: {
    params: Params<string>
}) => {
    const params = args.params as { docId: string };
    return { docId: params.docId };
}
type LoaderReturn = Awaited<ReturnType<typeof loader>>;


export default () => {
    const loaderReturn = useLoaderData() as LoaderReturn;
    const diagramName = "__doc__" + loaderReturn.docId;
    const [diagramContents, setDiagramContents] = React.useState<string>(localStorage.getItem(diagramName) ?? NEW_DOCUMENT);
    const [isErrorState, setIsErrorState] = React.useState<boolean>(false);
    React.useEffect(() => { localStorage.setItem(diagramName, diagramContents) }, [diagramContents]);
    return <>
        <h1>Document {loaderReturn.docId}</h1>
        <a href="/">Back</a>
        <div style={{ display: "flex" }}>
            <textarea style={{ width: "50vw", height: "80vh", background: isErrorState ? "pink" : "white" }} value={diagramContents} onChange={(evt) => setDiagramContents(evt.target.value)}></textarea>
            <Diagram
                setIsErrorState={setIsErrorState}
                diagramContents={diagramContents}
            />
        </div>
    </>
};

const Diagram = (props: {
    diagramContents: string,
    setIsErrorState: React.Dispatch<React.SetStateAction<boolean>>
}) => {
    const [lastSVG, setLastSVG] = React.useState<string>("");
    const [lastRenderedContents, setLastRenderedContents] = React.useState<string>("");
    const [inflightRequest, setInflightRequest] = React.useState<boolean>(false);
    React.useEffect(() => {
        (async () => {
            if (!inflightRequest && lastRenderedContents != props.diagramContents) {
                setInflightRequest(true)
                try {
                    const response = await fetch("http://localhost:5973/getDiagram", {
                        method: "post",
                        body: props.diagramContents
                    })
                    const plantUMLAndJson = await response.json();
                    props.setIsErrorState(false)
                    setLastSVG(plantUMLAndJson.svg);
                    setLastRenderedContents(props.diagramContents);
                } catch (error) {
                    props.setIsErrorState(true)
                    setLastRenderedContents(props.diagramContents);
                }
                setInflightRequest(false);
            }
        })();
    }, [
        props.diagramContents,
        inflightRequest
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


    return <ReactSvgPanZoomLoader svgXML={lastSVG} render={(content) => (
        <ReactSVGPanZoom
            width={800} height={800}
            tool={tool} onChangeTool={setTool}
            value={value} onChangeValue={setValue}
            detectAutoPan={false}
            background="white"
        >
            <svg width={500} height={500} >
                {content}
            </svg>
        </ReactSVGPanZoom>
    )} />
}

const NEW_DOCUMENT = `
hello sayto world

house has cat
house has mouse
cat eats mouse

* has *: contains
* eats *: -->:gotcha
`;