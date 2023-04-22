import React from 'react'
import { SvgLoader } from 'react-svgmt'
export const ReactSvgPanZoomLoader = (props) => {
    return (
        <div>
            {props.render(
                <SvgLoader path={props.src} svgXML={props.svgXML}>
                    {props.proxy}
                </SvgLoader>
            )}
        </div>
    )
}