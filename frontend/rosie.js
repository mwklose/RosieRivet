//tears of the team were shed here
import ReactDOM from 'react-dom';
import "@patternfly/react-core/dist/styles/base.css";
import './fonts.css';

import React from 'react';
import { FileUpload } from '@patternfly/react-core';
import FileUploadIcon from '@patternfly/react-icons/dist/js/icons/file-upload-icon';

class CustomPreviewFileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: null, filename: '' };
    this.handleFileChange = (value, filename, event) => this.setState({ value, filename });
  }

  render() {
    const { value, filename, isLoading } = this.state;
    return (
      <FileUpload
        id="customized-preview-file"
        value={value}
        filename={filename}
        onChange={this.handleFileChange}
        hideDefaultPreview
      >
        {value && (
          <div className="pf-u-m-md">
            <FileUploadIcon size="lg" /> Custom preview here for your {value.size}-byte file named {value.name}
          </div>
        )}
      </FileUpload>
    );
  }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<CustomPreviewFileUpload />, rootElement);
