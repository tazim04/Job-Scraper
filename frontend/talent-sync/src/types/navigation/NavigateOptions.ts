import { Page, SubPage } from "./Page";
import JobResult from "../JobResult";

export type NavigateOptions = {
  page: Page;
  subPage?: SubPage;
  data?: JobResult;
  update?: boolean;
};

export default NavigateOptions;
