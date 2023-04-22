import * as React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import DocViewer, { loader } from "~DocViewer";
import DocumentSelector from "~DocumentSelector";


const router = createBrowserRouter([
  {
    path: "/",
    element: <DocumentSelector/>,
  },
  {
    path: "docs/:docId",
    element: <DocViewer />,
    loader: loader
  },
]);

export default () => (
  <RouterProvider router={router} />
);
