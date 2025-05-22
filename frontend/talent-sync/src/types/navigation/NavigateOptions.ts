import { Page, SubPage } from "./Page";
import JobResult from "../jobResult";

export type NavigateOptions = {
  page: Page;
  subPage?: SubPage;
  data?: JobResult;
  update?: boolean;
};

export default NavigateOptions;
